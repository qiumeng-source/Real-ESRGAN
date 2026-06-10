# Real-ESRGAN 图像超分辨率与修复系统

本项目基于原始 Real-ESRGAN 推理能力，整理为适合课程项目展示的前后端分离结构。

- 前端：HTML / CSS / JavaScript
- 后端：Flask + Python
- 推理引擎：Real-ESRGAN

项目保留了原仓库中的 `realesrgan/`、`inference_realesrgan.py`、`weights/` 等核心代码与推理逻辑；新增的 `backend/` 和 `frontend/` 仅负责接口封装与页面展示，不会删除原有可运行的 Real-ESRGAN 核心实现。

## 技术栈

- 前端：原生 HTML、CSS、JavaScript
- 后端：Flask、flask-cors、Pillow
- 推理：RealESRGANer、BasicSR、OpenCV、PyTorch

## 项目结构

```text
Real-ESRGAN/
├─ backend/
│  ├─ app.py
│  ├─ config.py
│  ├─ requirements.txt
│  ├─ services/
│  │  ├─ __init__.py
│  │  └─ realesrgan_service.py
│  ├─ static/
│  │  ├─ uploads/
│  │  │  └─ .gitkeep
│  │  └─ results/
│  │     └─ .gitkeep
│  └─ README.md
├─ frontend/
│  ├─ index.html
│  ├─ css/
│  │  └─ style.css
│  ├─ js/
│  │  └─ main.js
│  └─ README.md
├─ realesrgan/
├─ inference_realesrgan.py
├─ weights/
├─ README.md
└─ .gitignore
```

## 环境建议

- Python：推荐 `3.9`
- NumPy：`1.26.4`
- OpenCV：`4.8.1.78`
- PyTorch：推荐使用 CUDA 12.1 对应版本

如果你需要手动安装当前项目验证过的 PyTorch 版本，可使用：

```bash
pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu121
```

然后安装项目依赖：

```bash
pip install -r backend/requirements.txt
python setup.py develop
```

## 后端启动方法

```bash
cd backend
python app.py
```

后端地址：`http://127.0.0.1:5000`

健康检查地址：`http://127.0.0.1:5000/api/health`

## 前端启动方法

```bash
cd frontend
python -m http.server 5500
```

前端地址：`http://127.0.0.1:5500`

## 单张图片增强使用方法

1. 启动后端和前端。
2. 打开 `http://127.0.0.1:5500`。
3. 进入“单张图片增强”页签。
4. 上传一张 `jpg`、`jpeg` 或 `png` 图片。
5. 选择模型、放大倍数、去噪强度和分块大小。
6. 点击“开始增强”。
7. 查看原图、增强图和局部细节对比图。
8. 下载增强结果和局部对比图。

## 批量图片增强使用方法

1. 进入“批量图片增强”页签。
2. 一次选择多张 `jpg`、`jpeg` 或 `png` 图片。
3. 可在列表中查看文件名、文件大小并移除单张图片。
4. 设置模型、放大倍数、去噪强度和分块大小。
5. 点击“开始批量增强”。
6. 处理完成后查看每张图片的结果卡片。
7. 分别下载增强图、局部对比图，或点击“打包下载全部结果”。

## 局部对比图说明

- 系统会在每张图片增强完成后自动生成一张局部细节对比图。
- 对比图保存位置：`backend/static/results/`
- 对比图采用自动中心裁剪方式：
  左侧为“原图局部”
  右侧为“增强后局部”
- 该图适合在课程答辩或演示时展示增强前后的细节差异。

## 常见错误处理

- Python 版本问题：建议优先使用 Python 3.9，不建议直接使用过新的 Python 3.14。
- BasicSR 与 torchvision 兼容问题：建议使用 README 中列出的 PyTorch / torchvision 版本组合。
- NumPy 2.x 兼容问题：本项目固定为 `numpy==1.26.4`，避免 BasicSR 相关兼容性错误。
- OpenCV 版本问题：本项目固定为 `opencv-python==4.8.1.78`。
- CUDA 是否可用：可在 Python 中执行 `import torch; print(torch.cuda.is_available())` 检查。
- 显存不足：请将分块大小调小，例如 `128` 或 `256`。
- 模型权重下载较慢：首次运行可能需要自动下载权重，请耐心等待。
- 结果图无法显示：请检查后端是否正常运行，浏览器能否访问 `/api/result/...`。

## 权重路径配置

如需手动修改模型权重目录，请编辑：

```text
backend/config.py
```

默认配置为：

```python
WEIGHTS_DIR = PROJECT_ROOT / "weights"
```

模型 URL、权重文件名、默认参数、允许格式、批量数量限制等也统一配置在 `backend/config.py` 中。

## Git 提交说明

- 应提交：源代码、配置文件、README、`.gitignore`
- 不应提交：`backend/static/uploads/` 中的上传图片、`backend/static/results/` 中的增强结果与对比图、zip 打包文件
