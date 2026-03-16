---
name: image-generate
description: 使用内置脚本实现文生图, 图生图(参考一张或多张图), 准备清晰具体的 `prompt`。
---

# Image Generate

## 适用场景

当需要根据文本描述生成图片时，使用该技能。支持两种模式：
1. **文生图**：仅使用文本描述生成图片
2. **图生图**：基于参考图生成相似风格的图片

## 使用步骤

### 1. 文生图（基本模式）
```bash
python scripts/image_generate.py "<prompt>"
```

### 2. 图生图（参考图模式）
```bash
# 使用公网 URL
python scripts/image_generate_with_ref.py "<prompt>" "https://example.com/image.jpg"

# 使用本地文件（自动转换为 Base64）
python scripts/image_generate_with_ref.py "<prompt>" "/path/to/local/image.jpg"

# 使用 Base64 编码（完整格式）
python scripts/image_generate_with_ref.py "<prompt>" "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg=="
```

## 认证与凭据来源

- 优先读取 `MODEL_IMAGE_API_KEY` 或 `ARK_API_KEY` 环境变量。
- 若未配置，将尝试使用 `VOLCENGINE_ACCESS_KEY` 与 `VOLCENGINE_SECRET_KEY` 获取 Ark API Key。

## 输出格式

- 输出生成的图片文件路径。
- 若调用失败，将打印错误信息。

## 示例

### 文生图示例
```bash
python scripts/image_generate.py "一只可爱的猫"
```

### 图生图示例
```bash
# 使用本地头像生成睡前照片
python scripts/image_generate_with_ref.py "一个亚洲女生，穿着舒适的居家服，窝在沙发里准备睡觉" "/root/.openclaw/workspace/avatars/banji.jpg"

# 使用公网图片生成相似风格
python scripts/image_generate_with_ref.py "一个美丽的风景" "https://example.com/scenery.jpg"
```

## 技术说明

### Base64 编码格式
本地图片使用 Base64 编码传输，格式为：
```
data:image/<图片格式>;base64,<Base64编码>
```

**注意**：
- `<图片格式>` 需小写（如 `png`, `jpeg`, `jpg`）
- `jpg` 格式需转换为 `jpeg`（`data:image/jpeg;base64,...`）

### 支持的文件格式
- PNG (.png)
- JPEG/JPG (.jpg, .jpeg)
- WebP (.webp)
