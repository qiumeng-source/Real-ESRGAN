import sys
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from PIL import Image, UnidentifiedImageError
from werkzeug.exceptions import RequestEntityTooLarge

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from config import (  # noqa: E402
    ALLOWED_EXTENSIONS,
    ALLOWED_IMAGE_FORMATS,
    DEBUG,
    DEFAULT_DENOISE_STRENGTH,
    DEFAULT_MODEL_NAME,
    DEFAULT_OUTSCALE,
    DEFAULT_TILE,
    HOST,
    MAX_BATCH_FILES,
    MAX_CONTENT_LENGTH,
    MODEL_CHOICES,
    PORT,
    RESULT_DIR,
    UPLOAD_DIR,
    ZIP_DIR,
)
from services.realesrgan_service import (  # noqa: E402
    create_result_zip,
    generate_comparison_image,
    upscale_image,
)


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
CORS(app)

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
RESULT_DIR.mkdir(parents=True, exist_ok=True)
ZIP_DIR.mkdir(parents=True, exist_ok=True)


def zh(text):
    return text.encode("utf-8").decode("unicode_escape")


def error_response(message, status_code=400, extra=None):
    payload = {
        "success": False,
        "original_url": None,
        "result_url": None,
        "download_url": None,
        "comparison_url": None,
        "comparison_download_url": None,
        "filename": None,
        "message": message,
    }
    if extra:
        payload.update(extra)
    response = jsonify(payload)
    response.status_code = status_code
    return response


def get_base_url():
    return request.host_url.rstrip("/")


def build_file_url(endpoint, filename):
    return f"{get_base_url()}{endpoint}/{filename}"


def generate_unique_filename(extension, suffix=""):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    tail = f"_{suffix}" if suffix else ""
    return f"{timestamp}_{uuid4().hex}{tail}.{extension}"


def parse_int(value, field_name, minimum=None):
    try:
        parsed = int(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{field_name} 必须是整数。") from error
    if minimum is not None and parsed < minimum:
        raise ValueError(f"{field_name} 不能小于 {minimum}。")
    return parsed


def parse_float(value, field_name, minimum=None, maximum=None):
    try:
        parsed = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{field_name} 必须是数字。") from error
    if minimum is not None and parsed < minimum:
        raise ValueError(f"{field_name} 不能小于 {minimum}。")
    if maximum is not None and parsed > maximum:
        raise ValueError(f"{field_name} 不能大于 {maximum}。")
    return parsed


def validate_image_file(file_storage):
    if file_storage is None or not file_storage.filename:
        raise ValueError(zh(r"\u8bf7\u5148\u4e0a\u4f20\u56fe\u7247\u6587\u4ef6\u3002"))

    original_extension = Path(file_storage.filename).suffix.lower().lstrip(".")
    if original_extension not in ALLOWED_EXTENSIONS:
        raise ValueError(zh(r"\u53ea\u652f\u6301 jpg\u3001jpeg\u3001png \u683c\u5f0f\u7684\u56fe\u7247\u3002"))

    try:
        image = Image.open(file_storage.stream)
        image.verify()
        actual_format = (image.format or "").lower()
    except (UnidentifiedImageError, OSError) as error:
        raise ValueError(zh(r"\u4e0a\u4f20\u7684\u6587\u4ef6\u4e0d\u662f\u6709\u6548\u56fe\u7247\u3002")) from error
    finally:
        file_storage.stream.seek(0)

    if actual_format not in ALLOWED_IMAGE_FORMATS:
        raise ValueError(zh(r"\u53ea\u652f\u6301 jpg\u3001jpeg\u3001png \u683c\u5f0f\u7684\u56fe\u7247\u3002"))

    return "jpg" if actual_format == "jpeg" else actual_format


def save_upload(file_storage, extension):
    filename = generate_unique_filename(extension)
    upload_path = UPLOAD_DIR / filename

    with Image.open(file_storage.stream) as image:
        save_image = image.copy()
        if extension == "jpg" and save_image.mode in ("RGBA", "LA", "P"):
            save_image = save_image.convert("RGB")
        save_image.save(upload_path)

    file_storage.stream.seek(0)
    return filename, upload_path


def build_result_item(original_name, original_filename, result_filename, comparison_filename, message):
    return {
        "success": True,
        "original_name": original_name,
        "original_url": build_file_url("/api/upload", original_filename),
        "result_url": build_file_url("/api/result", result_filename),
        "download_url": build_file_url("/api/download", result_filename),
        "comparison_url": build_file_url("/api/result", comparison_filename),
        "comparison_download_url": build_file_url("/api/download", comparison_filename),
        "filename": result_filename,
        "message": message,
    }


def process_single_file(file_storage, model_name, outscale, denoise_strength, tile):
    image_extension = validate_image_file(file_storage)
    original_name = file_storage.filename
    original_filename, upload_path = save_upload(file_storage, image_extension)
    result_filename = generate_unique_filename(image_extension, "result")
    result_path = RESULT_DIR / result_filename
    comparison_filename = generate_unique_filename("png", "comparison")
    comparison_path = RESULT_DIR / comparison_filename

    upscale_image(
        input_path=upload_path,
        output_path=result_path,
        model_name=model_name,
        outscale=outscale,
        denoise_strength=denoise_strength,
        tile=tile,
    )
    generate_comparison_image(upload_path, result_path, comparison_path)

    return build_result_item(
        original_name,
        original_filename,
        result_filename,
        comparison_filename,
        zh(r"\u56fe\u50cf\u589e\u5f3a\u6210\u529f\u3002"),
    )


def parse_request_params(form_data):
    model_name = form_data.get("model_name", DEFAULT_MODEL_NAME)
    if model_name not in MODEL_CHOICES:
        raise ValueError(
            zh(r"\u4e0d\u652f\u6301\u7684\u6a21\u578b\u540d\u79f0\u3002\u53ef\u9009\u6a21\u578b\uff1a")
            + ", ".join(MODEL_CHOICES)
        )

    outscale = parse_float(form_data.get("outscale", DEFAULT_OUTSCALE), zh(r"\u653e\u5927\u500d\u6570"), minimum=1)
    denoise_strength = parse_float(
        form_data.get("denoise_strength", DEFAULT_DENOISE_STRENGTH),
        zh(r"\u53bb\u566a\u5f3a\u5ea6"),
        minimum=0,
        maximum=1,
    )
    tile = parse_int(form_data.get("tile", DEFAULT_TILE), zh(r"\u5206\u5757\u5927\u5c0f"), minimum=0)
    return model_name, outscale, denoise_strength, tile


def get_batch_files():
    files = request.files.getlist("images")
    if not files:
        files = request.files.getlist("images[]")
    return [file for file in files if file and file.filename]


@app.errorhandler(RequestEntityTooLarge)
def handle_large_file(_error):
    return error_response(zh(r"\u4e0a\u4f20\u6587\u4ef6\u8fc7\u5927\uff0c\u8bf7\u538b\u7f29\u56fe\u7247\u540e\u91cd\u8bd5\u3002"), 413)


@app.get("/api/health")
def health():
    return jsonify(
        {
            "success": True,
            "message": zh(r"\u540e\u7aef\u8fd0\u884c\u6b63\u5e38\u3002"),
            "models": MODEL_CHOICES,
            "defaults": {
                "model_name": DEFAULT_MODEL_NAME,
                "outscale": DEFAULT_OUTSCALE,
                "denoise_strength": DEFAULT_DENOISE_STRENGTH,
                "tile": DEFAULT_TILE,
            },
        }
    )


@app.post("/api/upscale")
def upscale():
    try:
        model_name, outscale, denoise_strength, tile = parse_request_params(request.form)
        file_storage = request.files.get("image")
        result = process_single_file(file_storage, model_name, outscale, denoise_strength, tile)
        return jsonify(result)
    except ValueError as error:
        return error_response(str(error), 400)
    except Exception as error:
        return error_response(zh(r"\u5904\u7406\u5931\u8d25\uff1a") + str(error), 500)


@app.post("/api/batch-upscale")
def batch_upscale():
    try:
        model_name, outscale, denoise_strength, tile = parse_request_params(request.form)
        files = get_batch_files()

        if not files:
            raise ValueError(zh(r"\u8bf7\u81f3\u5c11\u4e0a\u4f20\u4e00\u5f20\u56fe\u7247\u3002"))
        if len(files) > MAX_BATCH_FILES:
            raise ValueError(f"单次最多上传 {MAX_BATCH_FILES} 张图片。")

        results = []
        zip_files = []

        for file_storage in files:
            try:
                item = process_single_file(file_storage, model_name, outscale, denoise_strength, tile)
                results.append(item)
                zip_files.append(RESULT_DIR / item["filename"])
                zip_files.append(RESULT_DIR / Path(item["comparison_url"]).name)
            except Exception as error:
                results.append(
                    {
                        "success": False,
                        "original_name": file_storage.filename,
                        "original_url": None,
                        "result_url": None,
                        "download_url": None,
                        "comparison_url": None,
                        "comparison_download_url": None,
                        "message": zh(r"\u5904\u7406\u5931\u8d25\uff1a") + str(error),
                    }
                )

        zip_filename = None
        zip_url = None
        zip_download_url = None
        if zip_files:
            zip_filename = generate_unique_filename("zip", "batch_results")
            zip_path = ZIP_DIR / zip_filename
            create_result_zip(zip_path, zip_files)
            zip_url = build_file_url("/api/download-zip", zip_filename)
            zip_download_url = zip_url

        return jsonify(
            {
                "success": True,
                "message": zh(r"\u6279\u91cf\u589e\u5f3a\u5b8c\u6210\u3002"),
                "results": results,
                "zip_url": zip_url,
                "zip_download_url": zip_download_url,
                "zip_filename": zip_filename,
            }
        )
    except ValueError as error:
        return error_response(str(error), 400, extra={"results": [], "zip_url": None, "zip_download_url": None})
    except Exception as error:
        return error_response(
            zh(r"\u6279\u91cf\u5904\u7406\u5931\u8d25\uff1a") + str(error),
            500,
            extra={"results": [], "zip_url": None, "zip_download_url": None},
        )


@app.get("/api/upload/<path:filename>")
def get_upload(filename):
    return send_from_directory(UPLOAD_DIR, filename)


@app.get("/api/result/<path:filename>")
def get_result(filename):
    return send_from_directory(RESULT_DIR, filename)


@app.get("/api/download/<path:filename>")
def download_result(filename):
    return send_from_directory(RESULT_DIR, filename, as_attachment=True)


@app.get("/api/download-zip/<path:filename>")
def download_zip(filename):
    return send_from_directory(ZIP_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)
