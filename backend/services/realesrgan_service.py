import zipfile
from pathlib import Path

import cv2
import torch
from PIL import Image, ImageDraw, ImageFont
from basicsr.archs.rrdbnet_arch import RRDBNet
from basicsr.utils.download_util import load_file_from_url

from realesrgan import RealESRGANer
from realesrgan.archs.srvgg_arch import SRVGGNetCompact

from config import MODEL_CONFIGS, WEIGHTS_DIR


def zh(text):
    return text.encode("utf-8").decode("unicode_escape")


def ensure_weights_dir():
    WEIGHTS_DIR.mkdir(parents=True, exist_ok=True)


def build_model(model_name):
    config = MODEL_CONFIGS.get(model_name)
    if config is None:
        raise ValueError(zh(r"\u4e0d\u652f\u6301\u7684\u6a21\u578b\uff1a") + model_name)

    if config["arch"] == "rrdbnet":
        model = RRDBNet(
            num_in_ch=3,
            num_out_ch=3,
            num_feat=64,
            num_block=config["num_block"],
            num_grow_ch=32,
            scale=config["netscale"],
        )
    elif config["arch"] == "srvgg":
        model = SRVGGNetCompact(
            num_in_ch=3,
            num_out_ch=3,
            num_feat=64,
            num_conv=config["num_conv"],
            upscale=config["netscale"],
            act_type="prelu",
        )
    else:
        raise ValueError(zh(r"\u4e0d\u652f\u6301\u7684\u6a21\u578b\u7ed3\u6784\uff1a") + str(config["arch"]))

    return model, config["netscale"], config["urls"], config["weight_name"]


def resolve_model_path(model_name, urls, weight_name):
    ensure_weights_dir()

    local_path = WEIGHTS_DIR / weight_name
    if local_path.exists():
        return str(local_path)

    latest_path = None
    for url in urls:
        latest_path = load_file_from_url(
            url=url,
            model_dir=str(WEIGHTS_DIR),
            progress=True,
            file_name=None,
        )

    if latest_path is None:
        raise FileNotFoundError(zh(r"\u672a\u80fd\u83b7\u53d6\u6a21\u578b\u6743\u91cd\uff1a") + model_name)

    return latest_path


def create_upsampler(model_name, denoise_strength, tile):
    model, netscale, urls, weight_name = build_model(model_name)
    model_path = resolve_model_path(model_name, urls, weight_name)

    dni_weight = None
    if model_name == "realesr-general-x4v3" and denoise_strength != 1:
        wdn_model_path = str(model_path).replace("realesr-general-x4v3", "realesr-general-wdn-x4v3")
        model_path = [model_path, wdn_model_path]
        dni_weight = [denoise_strength, 1 - denoise_strength]

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")

    return RealESRGANer(
        scale=netscale,
        model_path=model_path,
        dni_weight=dni_weight,
        model=model,
        tile=int(tile),
        tile_pad=10,
        pre_pad=0,
        half=use_cuda,
        device=device,
        gpu_id=0 if use_cuda else None,
    )


def upscale_image(input_path, output_path, model_name, outscale, denoise_strength, tile):
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.exists():
        raise FileNotFoundError(zh(r"\u8f93\u5165\u56fe\u7247\u4e0d\u5b58\u5728\uff1a") + str(input_path))

    image = cv2.imread(str(input_path), cv2.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError(zh(r"\u65e0\u6cd5\u8bfb\u53d6\u8f93\u5165\u56fe\u7247\uff1a") + str(input_path))

    upsampler = create_upsampler(model_name, denoise_strength, tile)

    try:
        output, _ = upsampler.enhance(image, outscale=float(outscale))
    except RuntimeError as error:
        raise RuntimeError(zh(r"\u63a8\u7406\u5931\u8d25\uff1a") + str(error) + zh(r"\u3002\u8bf7\u5c1d\u8bd5\u51cf\u5c0f tile \u5927\u5c0f\u3002")) from error

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(output_path), output):
        raise RuntimeError(zh(r"\u4fdd\u5b58\u589e\u5f3a\u7ed3\u679c\u5931\u8d25\uff1a") + str(output_path))

    return str(output_path)


def load_font(size):
    font_paths = [
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/simsun.ttc"),
    ]
    for font_path in font_paths:
        if font_path.exists():
            return ImageFont.truetype(str(font_path), size=size)
    return ImageFont.load_default()


def add_centered_label(draw, box, text, font, fill):
    text_box = draw.textbbox((0, 0), text, font=font)
    text_width = text_box[2] - text_box[0]
    text_height = text_box[3] - text_box[1]
    x = box[0] + (box[2] - box[0] - text_width) // 2
    y = box[1] + (box[3] - box[1] - text_height) // 2
    draw.text((x, y), text, font=font, fill=fill)


def generate_comparison_image(original_path, result_path, comparison_path, crop_ratio=0.45):
    original_path = Path(original_path)
    result_path = Path(result_path)
    comparison_path = Path(comparison_path)

    with Image.open(original_path) as original_image:
        original = original_image.convert("RGB")
    with Image.open(result_path) as result_image:
        enhanced = result_image.convert("RGB")

    orig_w, orig_h = original.size
    enh_w, enh_h = enhanced.size

    crop_w = max(1, min(orig_w, int(orig_w * crop_ratio)))
    crop_h = max(1, min(orig_h, int(orig_h * crop_ratio)))

    left = max(0, (orig_w - crop_w) // 2)
    top = max(0, (orig_h - crop_h) // 2)
    right = min(orig_w, left + crop_w)
    bottom = min(orig_h, top + crop_h)
    original_crop = original.crop((left, top, right, bottom))

    scale_x = enh_w / max(1, orig_w)
    scale_y = enh_h / max(1, orig_h)
    enhanced_box = (
        max(0, int(round(left * scale_x))),
        max(0, int(round(top * scale_y))),
        min(enh_w, int(round(right * scale_x))),
        min(enh_h, int(round(bottom * scale_y))),
    )
    enhanced_crop = enhanced.crop(enhanced_box)

    if enhanced_crop.width == 0 or enhanced_crop.height == 0:
        enhanced_crop = enhanced

    original_crop = original_crop.resize(enhanced_crop.size, Image.Resampling.LANCZOS)

    label_height = max(46, enhanced_crop.height // 9)
    gap = 10
    canvas_width = enhanced_crop.width * 2 + gap
    canvas_height = enhanced_crop.height + label_height

    canvas = Image.new("RGB", (canvas_width, canvas_height), "#f8fafc")
    canvas.paste(original_crop, (0, label_height))
    canvas.paste(enhanced_crop, (enhanced_crop.width + gap, label_height))

    draw = ImageDraw.Draw(canvas)
    font = load_font(max(18, min(34, label_height // 2)))
    draw.rounded_rectangle((0, 0, enhanced_crop.width, label_height - 6), radius=16, fill="#dbeafe")
    draw.rounded_rectangle(
        (enhanced_crop.width + gap, 0, canvas_width, label_height - 6),
        radius=16,
        fill="#ccfbf1",
    )
    add_centered_label(draw, (0, 0, enhanced_crop.width, label_height - 6), zh(r"\u539f\u56fe\u5c40\u90e8"), font, "#1d4ed8")
    add_centered_label(
        draw,
        (enhanced_crop.width + gap, 0, canvas_width, label_height - 6),
        zh(r"\u589e\u5f3a\u540e\u5c40\u90e8"),
        font,
        "#0f766e",
    )

    comparison_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(comparison_path, "PNG")
    return str(comparison_path)


def create_result_zip(zip_path, file_paths):
    zip_path = Path(zip_path)
    zip_path.parent.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in file_paths:
            current = Path(file_path)
            if current.exists():
                zip_file.write(current, arcname=current.name)

    return str(zip_path)
