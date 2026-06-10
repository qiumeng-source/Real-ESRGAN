from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
STATIC_DIR = BACKEND_DIR / "static"
UPLOAD_DIR = STATIC_DIR / "uploads"
RESULT_DIR = STATIC_DIR / "results"
ZIP_DIR = RESULT_DIR
WEIGHTS_DIR = PROJECT_ROOT / "weights"

HOST = "127.0.0.1"
PORT = 5000
DEBUG = True

MAX_CONTENT_LENGTH = 20 * 1024 * 1024
MAX_BATCH_FILES = 10

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}
ALLOWED_IMAGE_FORMATS = {"jpeg", "png"}

DEFAULT_MODEL_NAME = "RealESRGAN_x4plus"
DEFAULT_OUTSCALE = 4
DEFAULT_DENOISE_STRENGTH = 0.5
DEFAULT_TILE = 256

MODEL_CONFIGS = {
    "RealESRGAN_x4plus": {
        "arch": "rrdbnet",
        "netscale": 4,
        "num_block": 23,
        "weight_name": "RealESRGAN_x4plus.pth",
        "urls": [
            "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth",
        ],
    },
    "RealESRNet_x4plus": {
        "arch": "rrdbnet",
        "netscale": 4,
        "num_block": 23,
        "weight_name": "RealESRNet_x4plus.pth",
        "urls": [
            "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.1/RealESRNet_x4plus.pth",
        ],
    },
    "RealESRGAN_x4plus_anime_6B": {
        "arch": "rrdbnet",
        "netscale": 4,
        "num_block": 6,
        "weight_name": "RealESRGAN_x4plus_anime_6B.pth",
        "urls": [
            "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.2.4/RealESRGAN_x4plus_anime_6B.pth",
        ],
    },
    "RealESRGAN_x2plus": {
        "arch": "rrdbnet",
        "netscale": 2,
        "num_block": 23,
        "weight_name": "RealESRGAN_x2plus.pth",
        "urls": [
            "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth",
        ],
    },
    "realesr-animevideov3": {
        "arch": "srvgg",
        "netscale": 4,
        "num_conv": 16,
        "weight_name": "realesr-animevideov3.pth",
        "urls": [
            "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-animevideov3.pth",
        ],
    },
    "realesr-general-x4v3": {
        "arch": "srvgg",
        "netscale": 4,
        "num_conv": 32,
        "weight_name": "realesr-general-x4v3.pth",
        "urls": [
            "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-wdn-x4v3.pth",
            "https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.5.0/realesr-general-x4v3.pth",
        ],
    },
}

MODEL_CHOICES = list(MODEL_CONFIGS.keys())
