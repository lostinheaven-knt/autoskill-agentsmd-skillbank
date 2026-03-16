# Genstore Operation Skill 快速开始指南

## 概述
Genstore Operation Skill 是一个专门用于Digital Essence店铺自动化运营的技能。它集成了LUI（语言用户界面）和传统菜单操作，提供统一的自动化接口。

## 安装

### 前提条件
- Python 3.8+
- OpenClaw环境
- Genstore店铺管理员权限

### 安装步骤

#### 1. 复制技能文件
```bash
# 将技能目录复制到OpenClaw技能目录
cp -r genstore-operation ~/.openclaw/workspace/skills/
```

#### 2. 安装依赖
```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/genstore-operation

# 安装Python依赖（如果有的话）
# 当前版本没有外部依赖
```

#### 3. 配置店铺信息
编辑 `config.json` 文件，更新店铺信息：
```json
{
  "store": {
    "name": "你的店铺名称",
    "domain": "你的店铺域名",
    "admin_url": "你的后台管理地址",
    "login": {
      "email": "你的登录邮箱",
      "password_env": "GENSTORE_PASSWORD"
    }
  }
}
```

## 基本使用

### 1. 创建单个产品

#### 方法1: 使用LUI（推荐）
```python
from scripts.automation import GenstoreAutomation

# 初始化
automation = GenstoreAutomation()

# 创建产品数据
product_data = {
    "title": "AI写作助手 - 智能内容生成",
    "price": "$14.99",
    "description": "基于AI的智能写作工具",
    "features": ["AI内容生成", "语法检查", "风格调整"],
    "inventory": 100
}

# 创建产品
result = automation.create_product(product_data, method="lui")
print(result)
```

#### 方法2: 使用传统菜单
```python
result = automation.create_product(product_data, method="traditional")
print(result)
```

#### 方法3: 智能选择（自动）
```python
result = automation.create_product(product_data, method="auto")
print(result)
```

### 2. 批量创建产品
```python
# 产品数据列表
products_data = [
    {
        "title": "产品1",
        "price": "$9.99",
        "description": "产品1描述"
    },
    {
        "title": "产品2", 
        "price": "$19.99",
        "description": "产品2描述"
    }
]

# 批量创建
results = automation.batch_create_products(products_data)
print(f"批量创建结果: {len([r for r in results if r['success']])}/{len(results)} 成功")
```

### 3. 设计店铺首页
```python
# 设计首页
design_result = automation.design_homepage(
    style="未来科技风格",
    requirements="简洁现代，突出数字产品特色，响应式设计"
)
print(design_result)
```

### 4. 创建营销活动
```python
# 创建营销活动
campaign_data = {
    "name": "春季数字产品促销",
    "period": "3月15日-4月15日",
    "discount": "8折优惠"
}

campaign_result = automation.create_campaign(campaign_data)
print(campaign_result)
```

### 5. 检查店铺状态
```python
# 检查店铺状态
status_result = automation.check_store_status()
print(status_result)
```

### 6. 运行每日任务
```python
# 运行每日任务
daily_results = automation.run_daily_tasks()
print(f"每日任务执行完成: {len(daily_results)}个任务")
```

### 7. 生成报告
```python
# 生成日报
daily_report = automation.generate_report("daily")
print(daily_report)

# 生成周报
weekly_report = automation.generate_report("weekly")
print(weekly_report)

# 生成月报
monthly_report = automation.generate_report("monthly")
print(monthly_report)
```

## 命令行使用

### 创建产品
```bash
# 使用LUI创建产品
python scripts/automation.py --action create_product \
  --data '{"title": "AI产品示例", "price": "$9.99", "description": "AI产品描述"}' \
  --method lui

# 使用传统菜单创建产品
python scripts/automation.py --action create_product \
  --data '{"title": "传统产品示例", "price": "$19.99"}' \
  --method traditional
```

### 批量创建
```bash
python scripts/automation.py --action batch_create \
  --data '{"products": [{"title": "产品1", "price": "$9.99"}, {"title": "产品2", "price": "$19.99"}]}'
```

### 设计首页
```bash
python scripts/automation.py --action design_homepage \
  --data '{"style": "未来科技风格", "requirements": "简洁现代设计"}'
```

### 生成报告
```bash
python scripts/automation.py --action generate_report \
  --data '{"type": "daily"}'
```

## 使用模板

### 1. 使用预定义产品模板
```python
import json

# 加载产品模板
with open('templates/product_templates.json', 'r', encoding='utf-8') as f:
    templates = json.load(f)

# 使用AI工具模板
ai_template = templates['ai_tools']['mindflow_ai']

# 创建产品
result = automation.create_product(ai_template)
print(result)
```

### 2. 自定义产品模板
```python
# 创建自定义模板
custom_template = {
    "title": "自定义产品",
    "price": "$29.99",
    "description": "自定义产品描述",
    "features": ["功能1", "功能2", "功能3"],
    "category": "Custom Category",
    "tags": ["custom", "digital", "product"],
    "inventory": 50
}

# 保存到模板文件
# 可以添加到 templates/product_templates.json 中
```

## 高级功能

### 1. 自定义配置
编辑 `config.json` 文件可以自定义：
- 店铺信息
- 操作偏好（LUI优先或传统菜单优先）
- 自动化任务计划
- 监控和警报设置

### 2. 扩展功能
可以通过修改以下文件扩展功能：
- `scripts/lui_operations.py`: LUI相关操作
- `scripts/traditional_operations.py`: 传统菜单操作
- `scripts/automation.py`: 主自动化逻辑

### 3. 日志和监控
- 操作日志保存在 `operation_log.json`
- 系统日志保存在 `genstore_automation.log`
- 可以通过配置文件调整日志级别

## 故障排除

### 常见问题

#### Q1: LUI操作失败
**可能原因**：
- 页面未完全加载
- LUI输入框选择器变化
- 网络连接问题

**解决方法**：
1. 检查页面是否完全加载
2. 更新 `config.json` 中的选择器
3. 尝试使用传统菜单操作

#### Q2: 传统菜单操作失败
**可能原因**：
- 页面结构变化
- 按钮选择器不正确
- 权限问题

**解决方法**：
1. 检查页面结构是否变化
2. 更新选择器配置
3. 确认登录状态和权限

#### Q3: 产品创建失败但无错误信息
**可能原因**：
- 产品信息不完整
- 价格格式不正确
- 库存设置问题

**解决方法**：
1. 检查产品数据是否完整
2. 确保价格格式正确（如 "$9.99"）
3. 设置合理的库存数量

### 调试模式
```python
import logging

# 启用调试日志
logging.getLogger().setLevel(logging.DEBUG)

# 执行操作
result = automation.create_product(product_data)
```

## 最佳实践

### 1. 操作顺序
1. 先检查店铺状态
2. 使用模板创建产品
3. 验证产品创建结果
4. 定期运行每日任务
5. 定期生成报告

### 2. 错误处理
```python
try:
    result = automation.create_product(product_data)
    if result['success']:
        print("操作成功")
    else:
        print(f"操作失败: {result.get('error', '未知错误')}")
        # 尝试备用方法
        if result.get('method') == 'lui':
            print("尝试使用传统菜单...")
            result = automation.create_product(product_data, method='traditional')
except Exception as e:
    print(f"异常错误: {e}")
```

### 3. 性能优化
- 批量操作时添加适当间隔
- 使用模板减少重复配置
- 定期清理日志文件
- 监控内存和CPU使用

### 4. 安全考虑
- 不要将密码硬编码在配置文件中
- 使用环境变量存储敏感信息
- 定期更新配置文件
- 备份重要数据

## 更新和维护

### 1. 检查更新
定期检查技能目录是否有更新：
```bash
cd ~/.openclaw/workspace/skills/genstore-operation
git pull origin main  # 如果使用git管理
```

### 2. 备份配置
```bash
# 备份配置文件
cp config.json config.json.backup
cp templates/product_templates.json templates/product_templates.json.backup
```

### 3. 清理日志
```bash
# 清理旧日志文件
find . -name "*.log" -mtime +30 -delete
find . -name "operation_log.json" -size +10M -delete
```

## 获取帮助

### 1. 查看文档
- `SKILL.md`: 技能详细说明
- `docs/quick_start.md`: 快速开始指南（本文档）
- `docs/api_reference.md`: API参考文档

### 2. 查看示例
- `scripts/` 目录中的示例代码
- `templates/` 目录中的模板示例

### 3. 报告问题
如果遇到问题，请：
1. 查看日志文件获取详细信息
2. 尝试使用备用方法
3. 检查配置文件是否正确
4. 如果问题持续，记录详细错误信息

---

**版本**: 1.0.0  
**最后更新**: 2026年3月3日  
**作者**: 班吉

> 提示：本技能会持续优化，建议定期查看更新和最佳实践。
