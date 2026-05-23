import time
import zipfile
from pathlib import Path

import cv2
import gradio as gr
import numpy as np
import torch
from PIL import Image, ImageDraw, ImageFont

from basicsr.archs.rrdbnet_arch import RRDBNet
from basicsr.utils.download_util import load_file_from_url
from realesrgan import RealESRGANer
from realesrgan.archs.srvgg_arch import SRVGGNetCompact


ROOT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT_DIR / "outputs"
BATCH_OUTPUT_DIR = ROOT_DIR / "batch_outputs"
WEIGHT_DIR = ROOT_DIR / "weights"
MODEL_CHOICES = [
    "RealESRGAN_x4plus",
    "RealESRGAN_x4plus_anime_6B",
]


def build_model(model_name):
    model_name = model_name.split(".")[0]

    if model_name == "RealESRGAN_x4plus":
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
        netscale = 4
        urls = ["https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth"]

    elif model_name == "RealESRNet_x4plus":
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
        netscale = 4
        urls = ["https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.1/RealESRNet_x4plus.pth"]

    elif model_name == "RealESRGAN_x4plus_anime_6B":
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=6, num_grow_ch=32, scale=4)
        netscale = 4
        urls = ["https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth"]

    elif model_name == "RealESRGAN_x2plus":
        model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
        netscale = 2
        urls = ["https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth"]

    elif model_name == "realesr-animevideov3":
        model = SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=16, upscale=4, act_type="prelu")
        netscale = 4
        urls = ["https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-animevideov3.pth"]

    elif model_name == "realesr-general-x4v3":
        model = SRVGGNetCompact(num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=32, upscale=4, act_type="prelu")
        netscale = 4
        urls = [
            "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-wdn-x4v3.pth",
            "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth",
        ]

    else:
        raise ValueError(f"Unsupported model: {model_name}")

    return model, netscale, urls


def resolve_model_path(model_name, urls):
    WEIGHT_DIR.mkdir(parents=True, exist_ok=True)

    local_path = WEIGHT_DIR / f"{model_name}.pth"
    if local_path.exists():
        return str(local_path)

    latest_path = None
    for url in urls:
        latest_path = load_file_from_url(
            url=url,
            model_dir=str(WEIGHT_DIR),
            progress=True,
            file_name=None,
        )

    return latest_path


def create_upsampler(model_name, outscale, denoise_strength, tile):
    model, netscale, urls = build_model(model_name)
    model_path = resolve_model_path(model_name, urls)

    dni_weight = None
    if model_name == "realesr-general-x4v3" and denoise_strength != 1:
        wdn_model_path = str(model_path).replace("realesr-general-x4v3", "realesr-general-wdn-x4v3")
        model_path = [model_path, wdn_model_path]
        dni_weight = [denoise_strength, 1 - denoise_strength]

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")

    upsampler = RealESRGANer(
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

    return upsampler, outscale


def pil_to_cv2(image):
    if image.mode == "RGBA":
        arr = np.array(image)
        return cv2.cvtColor(arr, cv2.COLOR_RGBA2BGRA), "png"

    if image.mode in ("L", "I;16"):
        return np.array(image), "png"

    arr = np.array(image.convert("RGB"))
    return cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), "png"


def cv2_to_pil(image):
    if len(image.shape) == 2:
        return Image.fromarray(image)

    if image.shape[2] == 4:
        return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA))

    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


def save_output(output, extension, output_dir=OUTPUT_DIR, filename_prefix="realesrgan"):
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{filename_prefix}_{time.strftime('%Y%m%d_%H%M%S')}.{extension}"
    save_path = output_dir / filename
    cv2.imwrite(str(save_path), output)
    return str(save_path)


def safe_filename_stem(path, fallback):
    stem = Path(path).stem if path else fallback
    cleaned = "".join(char if char.isalnum() or char in ("-", "_") else "_" for char in stem)
    return cleaned.strip("_") or fallback


def load_chinese_font(size):
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


def create_comparison_crop(original_img, enhanced_img, save_path, crop_ratio=0.45):
    original = original_img.convert("RGB")
    enhanced = enhanced_img.convert("RGB")

    orig_w, orig_h = original.size
    enh_w, enh_h = enhanced.size
    crop_w = max(1, int(orig_w * crop_ratio))
    crop_h = max(1, int(orig_h * crop_ratio))

    left = max(0, (orig_w - crop_w) // 2)
    top = max(0, (orig_h - crop_h) // 2)
    right = min(orig_w, left + crop_w)
    bottom = min(orig_h, top + crop_h)
    original_crop = original.crop((left, top, right, bottom))

    scale_x = enh_w / orig_w
    scale_y = enh_h / orig_h
    enh_box = (
        max(0, int(round(left * scale_x))),
        max(0, int(round(top * scale_y))),
        min(enh_w, int(round(right * scale_x))),
        min(enh_h, int(round(bottom * scale_y))),
    )
    enhanced_crop = enhanced.crop(enh_box)

    if enhanced_crop.width == 0 or enhanced_crop.height == 0:
        enhanced_crop = enhanced

    original_crop = original_crop.resize(enhanced_crop.size, Image.Resampling.LANCZOS)

    label_height = max(44, enhanced_crop.height // 10)
    gap = 8
    canvas_w = enhanced_crop.width * 2 + gap
    canvas_h = enhanced_crop.height + label_height
    canvas = Image.new("RGB", (canvas_w, canvas_h), "#fff8fd")
    canvas.paste(original_crop, (0, label_height))
    canvas.paste(enhanced_crop, (enhanced_crop.width + gap, label_height))

    draw = ImageDraw.Draw(canvas)
    font = load_chinese_font(max(18, min(34, label_height // 2)))
    draw.rounded_rectangle((0, 0, enhanced_crop.width, label_height - 6), radius=16, fill="#dbeafe")
    draw.rounded_rectangle((enhanced_crop.width + gap, 0, canvas_w, label_height - 6), radius=16, fill="#fce7f3")
    add_centered_label(draw, (0, 0, enhanced_crop.width, label_height - 6), "原图局部", font, "#1e3a8a")
    add_centered_label(draw, (enhanced_crop.width + gap, 0, canvas_w, label_height - 6), "增强后局部", font, "#9d174d")

    save_path = Path(save_path)
    save_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(save_path, "PNG")
    return str(save_path)


def enhance_with_upsampler(input_image, upsampler, actual_outscale, output_dir=OUTPUT_DIR, filename_prefix="realesrgan"):
    cv2_image, extension = pil_to_cv2(input_image)

    try:
        output, _ = upsampler.enhance(cv2_image, outscale=actual_outscale)
    except RuntimeError as error:
        raise gr.Error(f"Inference failed: {error}. Try using a smaller tile size.") from error

    save_path = save_output(output, extension, output_dir=output_dir, filename_prefix=filename_prefix)
    restored_image = cv2_to_pil(output)

    return restored_image, save_path


def upscale_image(input_image, model_name, outscale, denoise_strength, tile):
    if input_image is None:
        raise gr.Error("请先上传一张图片。")

    upsampler, actual_outscale = create_upsampler(model_name, outscale, denoise_strength, tile)
    restored_image, save_path = enhance_with_upsampler(
        input_image,
        upsampler,
        actual_outscale,
        output_dir=OUTPUT_DIR,
        filename_prefix="realesrgan",
    )

    comparison_path = OUTPUT_DIR / f"comparison_{time.strftime('%Y%m%d_%H%M%S')}.png"
    create_comparison_crop(input_image, restored_image, comparison_path)

    return input_image, restored_image, save_path, str(comparison_path), str(comparison_path)


def batch_upscale_images(input_files, model_name, outscale, denoise_strength, tile):
    if not input_files:
        raise gr.Error("请先上传至少一张图片。")

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    batch_dir = BATCH_OUTPUT_DIR / timestamp
    enhanced_dir = batch_dir / "enhanced"
    comparison_dir = batch_dir / "comparisons"
    enhanced_dir.mkdir(parents=True, exist_ok=True)
    comparison_dir.mkdir(parents=True, exist_ok=True)

    upsampler, actual_outscale = create_upsampler(model_name, outscale, denoise_strength, tile)
    enhanced_paths = []
    comparison_paths = []

    for index, file_path in enumerate(input_files, start=1):
        original_path = str(file_path)
        stem = safe_filename_stem(original_path, f"image_{index:02d}")
        with Image.open(original_path) as image:
            input_image = image.copy()

        restored_image, enhanced_path = enhance_with_upsampler(
            input_image,
            upsampler,
            actual_outscale,
            output_dir=enhanced_dir,
            filename_prefix=f"{index:02d}_{stem}",
        )
        comparison_path = comparison_dir / f"{index:02d}_{stem}_comparison.png"
        create_comparison_crop(input_image, restored_image, comparison_path)

        enhanced_paths.append(enhanced_path)
        comparison_paths.append(str(comparison_path))

    zip_path = batch_dir / f"realesrgan_batch_{timestamp}.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        for path in enhanced_paths + comparison_paths:
            file_path = Path(path)
            zip_file.write(file_path, arcname=str(file_path.relative_to(batch_dir)))

    return enhanced_paths, comparison_paths, str(zip_path)


def build_parameter_hints():
    return """
    <div class="hint-box">
        <strong>参数建议</strong>
        <ul>
            <li>真实照片建议使用 RealESRGAN_x4plus。</li>
            <li>动漫/卡通图片建议使用 RealESRGAN_x4plus_anime_6B。</li>
            <li>显存不足时将 Tile Size 设置为 256 或 512。</li>
            <li>Denoise Strength 越大，降噪越强，但可能损失细节。</li>
        </ul>
    </div>
    """


def build_demo():
    device_text = "GPU CUDA" if torch.cuda.is_available() else "CPU"

    custom_css = """
    .gradio-container {
        min-height: 100vh;
        background:
            radial-gradient(circle at 12% 12%, rgba(252, 231, 243, 0.9), transparent 28%),
            radial-gradient(circle at 88% 18%, rgba(254, 249, 195, 0.95), transparent 26%),
            linear-gradient(135deg, #e0f2fe 0%, #f5e8ff 45%, #ffe4ef 100%) !important;
        font-family: "Microsoft YaHei", "PingFang SC", "Inter", sans-serif;
    }

    .main-wrap {
        max-width: 1320px;
        margin: 0 auto;
        padding: 28px 18px 36px;
    }

    .title-card {
        padding: 28px 32px;
        margin-bottom: 22px;
        border: 2px solid rgba(255, 255, 255, 0.86);
        border-radius: 28px;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.94), rgba(239, 246, 255, 0.82));
        box-shadow: 0 18px 42px rgba(91, 77, 160, 0.16);
    }

    .title-card h1 {
        margin: 0 0 10px;
        color: #312e81;
        font-size: 32px;
        line-height: 1.22;
        font-weight: 900;
        letter-spacing: 0;
    }

    .title-card p {
        margin: 0;
        color: #475569;
        font-size: 16px;
        line-height: 1.7;
    }

    .device-badge {
        display: inline-flex;
        align-items: center;
        margin-top: 14px;
        padding: 8px 14px;
        border-radius: 999px;
        color: #7c3aed;
        background: rgba(245, 243, 255, 0.95);
        font-size: 13px;
        font-weight: 800;
        box-shadow: inset 0 0 0 1px rgba(167, 139, 250, 0.26);
    }

    .tabs {
        border-radius: 24px !important;
    }

    .tab-nav button {
        border-radius: 999px !important;
        font-weight: 800 !important;
    }

    .param-card,
    .preview-card,
    .guide-panel {
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.78);
        border-radius: 22px;
        background: rgba(255, 255, 255, 0.74);
        box-shadow: 0 14px 34px rgba(76, 69, 139, 0.13);
        backdrop-filter: blur(14px);
    }

    .section-title h2,
    .section-title h3 {
        margin: 0 0 14px;
        color: #312e81;
        font-size: 18px;
        font-weight: 900;
        letter-spacing: 0;
    }

    .param-card .wrap,
    .preview-card .wrap,
    .guide-panel .wrap {
        border-radius: 16px !important;
    }

    .preview-card img,
    .preview-card canvas,
    .preview-card .image-container,
    .preview-card .gallery {
        border-radius: 18px !important;
        overflow: hidden;
    }

    .run-button button {
        min-height: 48px;
        border: none !important;
        border-radius: 999px !important;
        background: linear-gradient(135deg, #8b5cf6 0%, #ec4899 52%, #f59e0b 100%) !important;
        color: #ffffff !important;
        font-size: 16px !important;
        font-weight: 900 !important;
        box-shadow: 0 12px 24px rgba(236, 72, 153, 0.24);
    }

    .run-button button:hover {
        transform: translateY(-1px);
        box-shadow: 0 16px 30px rgba(139, 92, 246, 0.28);
    }

    .hint-box {
        margin-top: 16px;
        padding: 14px 16px;
        border-left: 5px solid #a78bfa;
        border-radius: 16px;
        background: rgba(245, 243, 255, 0.82);
        color: #4c1d95;
        font-size: 14px;
        line-height: 1.72;
    }

    .hint-box ul,
    .guide-panel ul {
        margin: 8px 0 0;
        padding-left: 18px;
    }

    .guide-panel {
        color: #334155;
        line-height: 1.8;
    }

    .guide-panel h3 {
        color: #312e81;
    }
    """

    with gr.Blocks(
        title="Real-ESRGAN 图像超分辨率增强系统",
        css=custom_css,
    ) as demo:
        with gr.Column(elem_classes=["main-wrap"]):
            gr.HTML(
                f"""
                <div class="title-card">
                    <h1>Real-ESRGAN 图像超分辨率增强系统 ✨</h1>
                    <p>支持单张增强、批量处理和局部对比图生成，适合课程项目演示图像超分辨率效果。</p>
                    <div class="device-badge">当前运行设备：{device_text}</div>
                </div>
                """
            )

            with gr.Tabs(elem_classes=["tabs"]):
                with gr.Tab("单张图片增强"):
                    with gr.Row(equal_height=False):
                        with gr.Column(scale=5, elem_classes=["param-card"]):
                            gr.Markdown("## 参数设置", elem_classes=["section-title"])
                            input_image = gr.Image(type="pil", label="上传图片", height=270)
                            model_name = gr.Dropdown(
                                choices=MODEL_CHOICES,
                                value="RealESRGAN_x4plus",
                                label="Model",
                            )
                            outscale = gr.Slider(minimum=1, maximum=8, value=4, step=0.5, label="Output Scale")
                            denoise_strength = gr.Slider(
                                minimum=0,
                                maximum=1,
                                value=0.3,
                                step=0.1,
                                label="Denoise Strength",
                            )
                            tile = gr.Slider(minimum=0, maximum=1024, value=0, step=64, label="Tile Size")
                            run_button = gr.Button("开始增强", variant="primary", elem_classes=["run-button"])
                            gr.HTML(build_parameter_hints())

                        with gr.Column(scale=7, elem_classes=["preview-card"]):
                            gr.Markdown("## 图像预览与结果下载", elem_classes=["section-title"])
                            with gr.Row():
                                original_preview = gr.Image(type="pil", label="原始图片预览", height=330)
                                restored_preview = gr.Image(type="pil", label="增强后图片预览", height=330)
                            comparison_preview = gr.Image(type="filepath", label="局部对比图", height=300)
                            with gr.Row():
                                download_file = gr.File(label="下载增强结果")
                                comparison_file = gr.File(label="下载局部对比图")

                    run_button.click(
                        fn=upscale_image,
                        inputs=[input_image, model_name, outscale, denoise_strength, tile],
                        outputs=[
                            original_preview,
                            restored_preview,
                            download_file,
                            comparison_preview,
                            comparison_file,
                        ],
                    )

                with gr.Tab("批量图片增强"):
                    with gr.Row(equal_height=False):
                        with gr.Column(scale=5, elem_classes=["param-card"]):
                            gr.Markdown("## 批量参数设置", elem_classes=["section-title"])
                            batch_files = gr.Files(
                                label="批量上传图片",
                                file_types=[".jpg", ".jpeg", ".png", ".webp"],
                                type="filepath",
                            )
                            batch_model_name = gr.Dropdown(
                                choices=MODEL_CHOICES,
                                value="RealESRGAN_x4plus",
                                label="Model",
                            )
                            batch_outscale = gr.Slider(
                                minimum=1,
                                maximum=8,
                                value=4,
                                step=0.5,
                                label="Output Scale",
                            )
                            batch_denoise_strength = gr.Slider(
                                minimum=0,
                                maximum=1,
                                value=0.3,
                                step=0.1,
                                label="Denoise Strength",
                            )
                            batch_tile = gr.Slider(minimum=0, maximum=1024, value=0, step=64, label="Tile Size")
                            batch_run_button = gr.Button(
                                "开始批量增强",
                                variant="primary",
                                elem_classes=["run-button"],
                            )
                            gr.HTML(build_parameter_hints())

                        with gr.Column(scale=7, elem_classes=["preview-card"]):
                            gr.Markdown("## 批量输出", elem_classes=["section-title"])
                            enhanced_gallery = gr.Gallery(
                                label="增强后图片预览 Gallery",
                                columns=2,
                                height=360,
                                object_fit="contain",
                            )
                            comparison_gallery = gr.Gallery(
                                label="局部对比图 Gallery",
                                columns=2,
                                height=360,
                                object_fit="contain",
                            )
                            zip_file = gr.File(label="打包下载 zip 文件")

                    batch_run_button.click(
                        fn=batch_upscale_images,
                        inputs=[
                            batch_files,
                            batch_model_name,
                            batch_outscale,
                            batch_denoise_strength,
                            batch_tile,
                        ],
                        outputs=[enhanced_gallery, comparison_gallery, zip_file],
                    )

                with gr.Tab("使用说明"):
                    with gr.Column(elem_classes=["guide-panel"]):
                        gr.Markdown(
                            """
                            ### 使用流程
                            1. 单张增强：上传一张图片，选择模型和参数，点击“开始增强”。
                            2. 批量增强：一次上传多张 jpg、jpeg、png 或 webp 图片，点击“开始批量增强”。
                            3. 局部对比图会自动截取图片中心区域，左侧为原图局部，右侧为增强后局部。

                            ### 参数建议
                            - 真实照片建议使用 RealESRGAN_x4plus。
                            - 动漫/卡通图片建议使用 RealESRGAN_x4plus_anime_6B。
                            - 显存不足时将 Tile Size 设置为 256 或 512。
                            - Denoise Strength 越大，降噪越强，但可能损失细节。
                            """
                        )

    return demo


if __name__ == "__main__":
    app = build_demo()
    app.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)
