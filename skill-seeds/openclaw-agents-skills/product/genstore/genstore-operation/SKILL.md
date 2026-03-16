# Genstore Operation Skill

## 概述
Genstore店铺运营自动化技能，专门用于Digital Essence店铺的自动化运营管理。

## 技能特点
- **LUI优先**：优先使用语言用户界面进行所有操作
- **自动化脚本**：提供可复用的自动化操作脚本
- **经验封装**：将实际操作经验封装为可调用函数
- **持续优化**：基于badcase和经验持续改进

## 使用场景
1. 新产品创建和上架
2. 店铺创建和上架
3. 营销活动设置
4. 店铺装修和设计优化  
5. 日常运营监控
6. 数据分析和报告生成

## 🧠 关键经验积累

### LUI探索成功经验（2026-03-05）
#### 问题：找不到`#chat-input-container`输入框
#### 解决方案：`snapshot --annotate`是关键触发步骤
#### 成功操作流程：
```bash
# 1. 打开首页
agent-browser open https://admin.genstore.ai/admin/bigsale-1f1o85026/home

# 2. 关键步骤：执行snapshot（可能触发页面状态变化）
agent-browser snapshot --annotate

# 3. 填充输入框
agent-browser fill "#chat-input-container" "需求描述"

# 4. 点击发送按钮
agent-browser click "#ai-home-sent-message"

# 5. 验证结果
agent-browser snapshot --annotate
agent-browser get url
```

#### 验证结果：
- **输入框一直存在**：之前没找到是因为页面状态问题
- **`snapshot`可能触发渲染**：让动态元素显示出来
- **URL会变化**：进入具体对话后URL变为`/home/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

#### 学习要点：
1. 操作前先执行`snapshot --annotate`确保页面状态正确
2. 输入框选择器：`#chat-input-container`
3. 发送按钮选择器：`#ai-home-sent-message`
4. 页面URL变化表示成功进入对话界面

## 核心功能

### 1. LUI操作基础
```python
# 基础LUI操作函数
def lui_send_message(message):
    """通过LUI发送消息给AI agent"""
    # 找到输入框 #chat-input-container
    # 输入消息
    # 点击发送按钮 #ai-home-sent-message
    pass

def lui_create_product(product_info):
    """通过LUI创建产品"""
    prompt = f"创建一个数字产品，标题：{product_info['title']}，价格：{product_info['price']}，描述：{product_info['description']}"
    return lui_send_message(prompt)
```

### 2. 传统菜单操作（备用）
```python
def traditional_create_product(product_info):
    """通过传统菜单创建产品（LUI不可用时使用）"""
    # 导航到产品管理页面
    # 点击Add product
    # 选择Digital products
    # 填写产品信息
    # 保存产品
    pass
```

### 3. 店铺装修
```python
def design_homepage(style, requirements):
    """设计店铺首页"""
    prompt = f"为我的店铺设计一个{style}风格的首页，要求：{requirements}"
    return lui_send_message(prompt)
```

### 4. 营销活动
```python
def create_campaign(campaign_info):
    """创建营销活动"""
    prompt = f"创建一个营销活动，名称：{campaign_info['name']}，时间：{campaign_info['period']}，折扣：{campaign_info['discount']}"
    return lui_send_message(prompt)
```

## 配置文件

### 店铺信息配置
```json
{
  "store": {
    "name": "Digital Essence",
    "url": "digital-essence-ai.genmystore.com",
    "admin_url": "https://admin.genstore.ai/admin/bigsale-1f1o85026",
    "login": {
      "email": "chengze.chen@weimob.com",
      "password": "***"
    }
  }
}
```

### 产品模板
```json
{
  "product_templates": {
    "ai_tool": {
      "category": "AI Tools",
      "type": "digital",
      "default_price": "$9.99-$49.99",
      "tags": ["ai", "digital", "subscription"]
    },
    "design_tool": {
      "category": "Design Tools", 
      "type": "digital",
      "default_price": "$19.99-$99.99",
      "tags": ["design", "creative", "software"]
    }
  }
}
```

## 使用示例

### 示例1：创建AI冥想产品
```bash
# 使用LUI创建产品
./genstore-operation create-product \
  --title "MindFlow AI - 智能冥想伴侣" \
  --price "$9.99" \
  --description "AI-powered personalized meditation plans" \
  --method lui
```

### 示例2：设计店铺首页
```bash
# 设计未来科技风格首页
./genstore-operation design-homepage \
  --style "future-tech" \
  --requirements "简洁现代，突出数字产品特色，响应式设计"
```

### 示例3：设置春季促销
```bash
# 创建营销活动
./genstore-operation create-campaign \
  --name "Digital Spring Renewal" \
  --period "2026-03-15 to 2026-04-15" \
  --discount "20%"
```

## 操作指南

### LUI操作步骤
1. **登录后台**：访问 `https://admin.genstore.ai/admin/bigsale-1f1o85026`
2. **打开Chat List**：点击页面中的"Chat List"按钮
3. **开始对话**：在 `#chat-input-container` 输入框中输入需求
4. **发送请求**：点击 `#ai-home-sent-message` 发送按钮
5. **等待处理**：AI agent会处理请求并显示结果
6. **确认操作**：根据需要点击Save/Publish等按钮

### 传统菜单操作步骤
1. **产品管理**：导航到 `/admin/bigsale-1f1o85026/products`
2. **添加产品**：点击"Add product"按钮
3. **选择类型**：选择"Digital products"
4. **填写信息**：填写标题、价格、描述等信息
5. **设置库存**：设置库存数量（数字产品也需要设置）
6. **保存产品**：点击"Save"按钮

## 常见问题解决

### Q1: 找不到LUI输入框？
**解决方法**：
1. 确保页面完全加载
2. 查找 `#chat-input-container` 元素
3. 检查是否有"Tell your Al team what you want to build"提示
4. 刷新页面重试

### Q2: Save/Publish按钮不可点击？
**解决方法**：
1. 等待LUI任务完成
2. 检查是否有错误提示
3. 刷新页面重试
4. 使用传统菜单作为备用方案

### Q3: 产品创建失败？
**解决方法**：
1. 检查产品信息是否完整
2. 确保价格格式正确
3. 设置库存数量
4. 查看错误提示并调整

## 最佳实践

### 1. 优先使用LUI
- 所有操作尽量通过对话完成
- 提供清晰具体的需求描述
- 利用AI的创意和自动化能力

### 2. 保持记录
- 记录所有操作步骤
- 保存成功和失败的案例
- 持续优化操作脚本

### 3. 定期维护
- 每月检查店铺设置
- 更新产品信息和价格
- 优化店铺设计和用户体验

## 开发计划

### 第一阶段（基础功能）
- [x] LUI基础操作封装
- [x] 产品创建功能
- [x] 配置文件管理

### 第二阶段（高级功能）
- [ ] 自动化装修脚本
- [ ] 营销活动管理
- [ ] 数据分析报告

### 第三阶段（AI增强）
- [ ] 智能产品推荐
- [ ] 自动优化建议
- [ ] 预测性运营

## 文件结构
```
genstore-operation/
├── SKILL.md              # 技能说明文件
├── config.json          # 配置文件
├── scripts/             # 操作脚本
│   ├── lui_operations.py
│   ├── traditional_operations.py
│   └── automation.py
├── templates/           # 模板文件
│   ├── product_templates.json
│   └── campaign_templates.json
└── docs/               # 文档
    ├── quick_start.md
    └── api_reference.md
```

## 贡献指南
1. 所有操作经验应记录在docs/experience.md中
2. 发现的badcase记录在docs/badcases.md中  
3. 新功能开发前先更新开发计划
4. 保持代码和文档同步更新

## 许可证
MIT License

## 更新日志

### v1.0.0 (2026-03-03)
- 初始版本发布
- 包含基础LUI和传统操作
- 支持产品创建功能
- 提供配置管理和模板

---

**创建者：班吉**  
**创建时间：2026年3月3日**  
**最后更新：2026年3月3日**

> 提示：本技能会持续优化，建议定期查看更新。
