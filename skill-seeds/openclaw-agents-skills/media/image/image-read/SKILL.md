---
name: image-read
description: 使用 doubao-seed-2.0-code 模型进行图像理解。当用户需要理解图像内容、描述图片、分析图像中的物体或场景时使用此技能。注意：base_url 必须使用 coding plan 的 URL (https://ark.cn-beijing.volces.com/api/coding/v3)。
---

# Image Read - 图像理解技能

## 概述

本技能使用 `doubao-seed-2.0-code` 模型进行图像理解。虽然该模型在其他方面可能表现一般，但在图像理解方面有专长。**重要配置**：必须使用 coding plan 的 base_url：`https://ark.cn-beijing.volces.com/api/coding/v3`。

## 快速开始

### 环境要求
1. 设置 `ARK_API_KEY` 环境变量：
   ```bash
   export ARK_API_KEY='your-api-key'
   ```

2. 安装依赖：
   ```bash
   pip install openai
   ```

### 基本使用

使用 `scripts/image_understand.py` 脚本进行图像理解：

```bash
# 基本用法
python scripts/image_understand.py "https://example.com/image.jpg"

# 自定义问题
python scripts/image_understand.py "https://example.com/image.jpg" "这张图片中有什么物体？"

# 在 Python 代码中使用
from scripts.image_understand import read_image

result = read_image(
    image_url="https://example.com/image.jpg",
    question="请精确仔细描述一下这张图",
    model="doubao-seed-2.0-code"
)

if result["success"]:
    print(result["response"])
else:
    print(f"错误: {result['error']}")
```

## 核心功能

### 1. 图像描述
自动生成图像的详细描述，包括：
- 主要物体和场景
- 颜色、光线、构图
- 情感和氛围
- 细节特征

### 2. 问题回答
针对图像内容回答特定问题，例如：
- "图片中有什么物体？"
- "这张图片是在哪里拍摄的？"
- "图片中的人物在做什么？"
- "图片的颜色搭配如何？"

### 3. 多模态分析
结合视觉和文本理解，提供综合分析。

## 配置说明

### 重要配置项
- **base_url**: `https://ark.cn-beijing.volces.com/api/coding/v3` (必须使用 coding plan 的 URL)
- **模型**: `doubao-seed-2.0-code` (图像理解专用)
- **API Key**: 从环境变量 `ARK_API_KEY` 读取

### 错误处理
脚本包含完整的错误处理：
- API Key 未设置
- 网络连接问题
- API 调用失败
- 图像 URL 无效

## [TODO: Replace with the first main section based on chosen structure]

[TODO: Add content here. See examples in existing skills:
- Code samples for technical skills
- Decision trees for complex workflows
- Concrete examples with realistic user requests
- References to scripts/templates/references as needed]

## Resources (optional)

Create only the resource directories this skill actually needs. Delete this section if no resources are required.

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Examples from other skills:**
- PDF skill: `fill_fillable_fields.py`, `extract_form_field_info.py` - utilities for PDF manipulation
- DOCX skill: `document.py`, `utilities.py` - Python modules for document processing

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read by Codex for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Codex's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Codex should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Codex produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Not every skill requires all three types of resources.**
