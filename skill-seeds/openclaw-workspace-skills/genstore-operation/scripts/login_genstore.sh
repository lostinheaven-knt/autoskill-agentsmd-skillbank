#!/bin/bash
# Genstore登录脚本

echo "开始登录Genstore后台..."

# 1. 打开登录页面
agent-browser open "https://admin.genstore.ai/admin/bigsale-1f1o85026"

# 等待页面加载
sleep 3

echo "页面已打开，检查是否需要登录..."

# 检查页面标题或内容（这里需要实际检查）
# 如果出现登录表单，需要填写凭据

# 2. 检查是否需要登录（这里需要实际判断）
# 如果页面显示登录表单，执行以下操作：

# 查找邮箱输入框并输入
# agent-browser type "#email-input" "chengze.chen@weimob.com"

# 查找密码输入框并输入  
# agent-browser type "#password-input" "lostlostlostlost"

# 点击登录按钮
# agent-browser click "#login-button"

# 等待登录完成
# sleep 5

echo "登录过程完成（或不需要登录）"

# 3. 检查是否登录成功，进入后台
echo "尝试检查后台页面..."

# 4. 寻找Chat List入口
echo "寻找Chat List按钮..."

# 可能的Chat List入口：
# - 侧边栏菜单
# - 顶部导航
# - 特定按钮

# 5. 点击Chat List进入LUI界面
# agent-browser click "#chat-list-button"

echo "登录脚本执行完成"
echo "下一步：手动检查页面状态，寻找LUI输入框"