---
name: feishu-api-operation
description: 专门用于飞书API操作的技能，封装了发送图片、语音等媒体文件的两步法操作，提供完整的配置说明、示例代码和问题排查指南。
---

# Feishu API Operation Skill


## 核心发现
飞书API发送媒体文件必须通过两步完成：
1. **上传文件**：获取唯一标识（`image_key` / `file_key`）
2. **发送消息**：在消息内容中引用该标识

### 接口对照
| 媒体类型 | 上传接口 | 消息类型 | 引用字段 |
|---------|---------|---------|---------|
| 图片 | `POST /im/v1/images` | `image` | `image_key` |
| 语音 | `POST /im/v1/files` | `audio` | `file_key` |
| 其他文件 | `POST /im/v1/files` | 根据类型 | `file_key` |

---

## 配置要求

### 权限
- **图片上传**：`im:image`
- **文件上传**：获取与上传图片或文件资源
- **消息发送**：发送消息权限

### 环境变量
```json
// openclaw.json 或环境配置
FEISHU_APP_ID=your_app_id
FEISHU_APP_SECRET=your_app_secret
```

### 接收者 open_id
**注意**：`open_id` 必须与当前应用匹配，否则会报 `open_id cross app` 错误。  
✅ 正确示例：`ou_cffdc0ae4ef4e314a9b7e3133c6d817d`（需在 feishu-allowFrom.json 中授权）

---

## 使用示例

### 1. 获取 tenant_access_token
```bash
curl -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
  -H "Content-Type: application/json" \
  -d '{"app_id": "<FEISHU_APP_ID>", "app_secret": "<FEISHU_APP_SECRET>"}'
```

### 2. 发送图片
```bash
# 第一步：上传图片
curl -X POST https://open.feishu.cn/open-apis/im/v1/images \
  -H "Authorization: Bearer <tenant_access_token>" \
  -F "image_type=message" \
  -F "image=@/path/to/image.png"

# 第二步：发送消息
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer <tenant_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "receive_id": "ou_cffdc0ae4ef4e314a9b7e3133c6d817d",
    "msg_type": "image",
    "content": "{\"image_key\": \"<image_key>\"}"
  }'
```

### 3. 发送语音
```bash
# 第一步：上传语音文件（AMR格式）
curl -X POST https://open.feishu.cn/open-apis/im/v1/files \
  -H "Authorization: Bearer <tenant_access_token>" \
  -F "file_type=stream" \
  -F "file=@/path/to/audio.amr"

# 第二步：发送语音消息
curl -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer <tenant_access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "receive_id": "ou_cffdc0ae4ef4e314a9b7e3133c6d817d",
    "msg_type": "audio",
    "content": "{\"file_key\": \"<file_key>\"}"
  }'
```

### Python 实现
参考 `scripts/feishu_api.py`（封装了上传和发送方法）

---

## 问题排查

### 常见错误
- **400**：参数错误或权限不足
- **99992361**：`open_id cross app` – open_id 不属于当前应用
- **权限错误**：检查应用是否已开通相应权限

### 调试步骤
1. 确认 `tenant_access_token` 有效（2小时有效期）
2. 验证 `open_id` 是否在应用的授权列表中
3. 检查文件格式和大小（图片建议 <10MB，语音支持 AMR/M4A）
4. 查阅[飞书API错误码文档](https://open.feishu.cn/document/server-docs/docs)

---

## 文件位置
- **技能目录**：`/root/.openclaw/workspace/skills/feishu-api-operation/`
- **配置文件**：`/root/.openclaw/openclaw.json`
- **用户权限**：`/root/.openclaw/credentials/feishu-allowFrom.json`

---

## 注意事项
- **文件格式**：图片 PNG/JPG；语音 AMR/M4A
- **文件大小**：遵守飞书限制（通常图片 ≤10MB，语音 ≤20MB）
- **token 有效期**：2小时，过期需重新获取
- **权限预配**：必须在飞书开发者后台为应用添加权限并版本发布

---

**创建者**：班吉  
**学习指导**：菜头  
**应用场景**：日常自动化媒体消息推送