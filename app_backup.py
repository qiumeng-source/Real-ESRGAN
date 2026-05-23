import time
from pathlib import Path

import cv2
import gradio as gr
import numpy as np
import torch
from PIL import Image

from basicsr.archs.rrdbnet_arch import RRDBNet
from basicsr.utils.download_util import load_file_from_url
from realesrgan import RealESRGANer
from realesrgan.archs.srvgg_arch import SRVGGNetCompact


ROOT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT_DIR / "outputs"
WEIGHT_DIR = ROOT_DIR / "weights"


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


def save_output(output, extension):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"realesrgan_{time.strftime('%Y%m%d_%H%M%S')}.{extension}"
    save_path = OUTPUT_DIR / filename
    cv2.imwrite(str(save_path), output)
    return str(save_path)


def upscale_image(input_image, model_name, outscale, denoise_strength, tile):
    if input_image is None:
        raise gr.Error("Please upload an image first.")

    cv2_image, extension = pil_to_cv2(input_image)
    upsampler, actual_outscale = create_upsampler(model_name, outscale, denoise_strength, tile)

    try:
        output, _ = upsampler.enhance(cv2_image, outscale=actual_outscale)
    except RuntimeError as error:
        raise gr.Error(f"Inference failed: {error}. Try using a smaller tile size.") from error

    save_path = save_output(output, extension)
    restored_image = cv2_to_pil(output)

    return input_image, restored_image, save_path


def build_demo():
    device_text = "GPU CUDA" if torch.cuda.is_available() else "CPU"

    with gr.Blocks(title="Real-ESRGAN Image Super Resolution") as demo:
        gr.Markdown(f"# Real-ESRGAN Image Super Resolution\nCurrent device: **{device_text}**")

        with gr.Row():
            with gr.Column():
                input_image = gr.Image(type="pil", label="Upload Image")

                model_name = gr.Dropdown(
                    choices=[
                        "RealESRGAN_x4plus",
                        "RealESRNet_x4plus",
                        "RealESRGAN_x4plus_anime_6B",
                        "RealESRGAN_x2plus",
                        "realesr-animevideov3",
                        "realesr-general-x4v3",
                    ],
                    value="RealESRGAN_x4plus",
                    label="Model",
                )

                outscale = gr.Slider(minimum=1, maximum=8, value=4, step=0.5, label="Output Scale")
                denoise_strength = gr.Slider(minimum=0, maximum=1, value=0.5, step=0.1, label="Denoise Strength")
                tile = gr.Slider(minimum=0, maximum=1024, value=0, step=64, label="Tile Size")

                run_button = gr.Button("Start", variant="primary")

            with gr.Column():
                original_preview = gr.Image(type="pil", label="Original Image")
                restored_preview = gr.Image(type="pil", label="Enhanced Image")
                download_file = gr.File(label="Download Result")

        run_button.click(
            fn=upscale_image,
            inputs=[input_image, model_name, outscale, denoise_strength, tile],
            outputs=[original_preview, restored_preview, download_file],
        )

    return demo


if __name__ == "__main__":
    app = build_demo()
    app.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)
