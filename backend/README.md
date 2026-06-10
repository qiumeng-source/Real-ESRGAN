# 后端说明

后端使用 Flask 提供 API，不再渲染 HTML 模板页面。前端通过 `fetch` 调用这些接口完成图片增强、批量增强、结果展示与下载。

## 启动方式

```bash
cd backend
python app.py
```

后端地址：`http://127.0.0.1:5000`

健康检查：`http://127.0.0.1:5000/api/health`

## 接口说明

### `GET /api/health`

返回后端运行状态、可选模型列表和默认参数。

### `POST /api/upscale`

单张图片增强接口，使用 `multipart/form-data`：

- `image`
- `model_name`
- `outscale`
- `denoise_strength`
- `tile`

返回字段包括：

- `success`
- `original_url`
- `result_url`
- `download_url`
- `comparison_url`
- `comparison_download_url`
- `filename`
- `message`

### `POST /api/batch-upscale`

批量图片增强接口，使用 `multipart/form-data`：

- `images` 或 `images[]`
- `model_name`
- `outscale`
- `denoise_strength`
- `tile`

返回字段包括：

- `success`
- `message`
- `results`
- `zip_url`
- `zip_download_url`

### `GET /api/result/<filename>`

用于前端展示增强结果图或局部对比图。

### `GET /api/download/<filename>`

用于下载单张增强结果图或局部对比图。

### `GET /api/download-zip/<filename>`

用于下载批量处理结果的 zip 文件。

## 存储目录

- 上传目录：`backend/static/uploads/`
- 结果目录：`backend/static/results/`
- ZIP 输出目录：`backend/static/results/`

## 配置位置

统一配置文件：

```text
backend/config.py
```

包括以下内容：

- 上传目录
- 结果目录
- ZIP 目录
- 最大上传文件大小
- 批量最大文件数量
- 允许的图片格式
- 模型配置
- 默认参数

## 依赖说明

建议使用 Python 3.9。

当前依赖中已固定：

- `numpy==1.26.4`
- `opencv-python==4.8.1.78`
- `torch==2.1.2`
- `torchvision==0.16.2`

如果需要 CUDA 12.1 版本的 PyTorch，建议先执行：

```bash
pip install torch==2.1.2 torchvision==0.16.2 torchaudio==2.1.2 --index-url https://download.pytorch.org/whl/cu121
```

再执行：

```bash
pip install -r requirements.txt
python ../setup.py develop
```
