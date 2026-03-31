---
name: video-read
description: 使用 doubao-seed-2.0-code 模型进行视频理解。当用户需要理解视频内容、描述视频场景、分析视频中的动作或事件时使用此技能。注意：base_url 必须使用 coding plan 的 URL (https://ark.cn-beijing.volces.com/api/coding/v3)，SDK 使用 volcenginesdkarkruntime（不是 openai）。
---

# Video Read - 视频理解技能

## 概述

本技能使用 `doubao-seed-2.0-code` 模型进行视频理解。虽然该模型在其他方面可能表现一般，但在多模态理解方面有专长。**重要配置**：必须使用 coding plan 的 base_url：`https://ark.cn-beijing.volces.com/api/coding/v3`，SDK 使用 `volcenginesdkarkruntime`。

## 快速开始

### 环境要求
1. 设置 `ARK_API_KEY` 环境变量：
   ```bash
   export ARK_API_KEY='your-api-key'
   ```

2. 安装依赖（已预装）：
   ```bash
   # SDK 已预装：volcenginesdkarkruntime
   ```

### 基本使用

使用 `scripts/video_understand.py` 脚本进行视频理解：

```bash
# 基本用法
python scripts/video_understand.py "https://example.com/video.mp4"

# 自定义问题和 FPS
python scripts/video_understand.py "https://example.com/video.mp4" "视频中发生了什么？" 3

# 在 Python 代码中使用
from scripts.video_understand import read_video

result = read_video(
    video_url="https://example.com/video.mp4",
    question="请描述视频内容",
    model="doubao-seed-2.0-code",
    fps=2
)

if result["success"]:
    print(result["response"])
else:
    print(f"错误: {result['error']}")
```

## 核心功能

### 1. 视频内容描述
自动生成视频的详细描述，包括：
- 主要场景和背景
- 人物动作和行为
- 事件发展过程
- 情感和氛围

### 2. 问题回答
针对视频内容回答特定问题，例如：
- "视频中发生了什么？"
- "人物在做什么？"
- "场景在哪里？"
- "视频的主题是什么？"

### 3. FPS 控制
通过 `fps` 参数控制视频帧采样率：
- 默认：2 FPS（平衡性能与效果）
- 可调范围：根据视频长度和复杂度调整

### 4. 多模态分析
结合视觉、时序和文本理解，提供综合分析。

## 配置说明

### 重要配置项
- **base_url**: `https://ark.cn-beijing.volces.com/api/coding/v3` (必须使用 coding plan 的 URL)
- **SDK**: `volcenginesdkarkruntime`（不是 openai）
- **模型**: `doubao-seed-2.0-code`（视频理解专用）
- **API Key**: 从环境变量 `ARK_API_KEY` 读取

### 费用优化
- 优先使用 coding plan 的 URL（用户已订阅三个月火山云 coding plan）
- 合理设置 FPS 参数，避免不必要的 token 消耗

### 错误处理
脚本包含完整的错误处理：
- API Key 未设置
- 网络连接问题
- API 调用失败
- 视频 URL 无效
- 视频下载超时

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
