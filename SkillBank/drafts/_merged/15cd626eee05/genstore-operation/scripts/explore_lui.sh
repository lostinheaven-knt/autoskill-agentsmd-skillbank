#!/bin/bash
# LUI探索脚本

echo "===== LUI探索开始 ====="
echo "时间: $(date)"
echo "店铺: Digital Essence (bigsale-1f1o85026)"
echo "目标: 找到LUI输入框，测试LUI功能"
echo ""

# 1. 打开Genstore后台
echo "步骤1: 打开Genstore后台..."
agent-browser open "https://admin.genstore.ai/admin/bigsale-1f1o85026"

echo "等待页面加载..."
sleep 5

# 2. 检查是否需要登录
echo "步骤2: 检查页面状态..."
echo "检查是否有登录表单..."

# 这里需要实际检查页面内容
# 如果出现登录表单，需要填写凭据

# 可能的登录表单元素：
# - 邮箱输入框: input[type="email"], #email, .email-input
# - 密码输入框: input[type="password"], #password, .password-input  
# - 登录按钮: button[type="submit"], #login-button, .login-btn

echo "如果看到登录表单，请手动输入凭据:"
echo "- 邮箱: chengze.chen@weimob.com"
echo "- 密码: ********"
echo ""

# 3. 寻找Chat List入口
echo "步骤3: 寻找Chat List入口..."
echo "可能的Chat List位置:"
echo "- 侧边栏菜单 (sidebar)"
echo "- 顶部导航 (top navigation)"
echo "- 特定按钮或图标"
echo "- 可能叫做 'AI Assistant', 'Chat', 'LUI' 等"
echo ""

# 4. 进入Chat List/LUI界面
echo "步骤4: 点击Chat List进入LUI界面..."
echo "尝试点击可能的元素:"
echo "- #chat-list-button"
echo "- .chat-icon"
echo "- [data-testid='chat-button']"
echo "- 包含'Chat'文本的链接或按钮"
echo ""

# 5. 寻找LUI输入框
echo "步骤5: 寻找LUI输入框..."
echo "目标选择器: #chat-input-container"
echo "其他可能的选择器:"
echo "- .chat-input"
echo "- textarea[placeholder*='message']"
echo "- input[type='text']"
echo "- .message-input"
echo ""

# 6. 测试LUI功能
echo "步骤6: 测试LUI功能..."
echo "如果找到输入框，测试以下命令:"
echo "1. 'hello' - 基础测试"
echo "2. 'help' - 获取帮助"
echo "3. 'create a new product' - 测试产品创建"
echo "4. 'show me product list' - 测试查询功能"
echo ""

# 7. 记录结果
echo "步骤7: 记录探索结果..."
echo "请记录以下信息:"
echo "- 是否找到输入框: 是/否"
echo "- 输入框选择器: [具体选择器]"
echo "- LUI响应情况: [响应内容]"
echo "- 遇到的问题: [问题描述]"
echo "- 解决方案: [解决方法]"
echo ""

echo "===== LUI探索脚本结束 ====="
echo "请根据实际情况执行上述步骤"
echo "重要发现请及时记录到技能文档"