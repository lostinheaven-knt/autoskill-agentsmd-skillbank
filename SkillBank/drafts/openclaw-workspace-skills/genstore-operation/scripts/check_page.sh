#!/bin/bash
# 检查页面元素脚本

echo "检查当前页面状态..."

# 1. 检查页面标题
echo "尝试获取页面标题..."
agent-browser eval "document.title" 2>&1

echo "---"

# 2. 检查是否有登录表单
echo "检查登录表单元素..."
echo "检查input[type='email']:"
agent-browser eval "document.querySelector('input[type=\"email\"]') ? '找到邮箱输入框' : '未找到邮箱输入框'" 2>&1

echo "检查input[type='password']:"
agent-browser eval "document.querySelector('input[type=\"password\"]') ? '找到密码输入框' : '未找到密码输入框'" 2>&1

echo "检查button[type='submit']:"
agent-browser eval "document.querySelector('button[type=\"submit\"]') ? '找到提交按钮' : '未找到提交按钮'" 2>&1

echo "---"

# 3. 检查是否有其他登录相关元素
echo "检查其他可能的选择器..."
for selector in "#email" "#password" "#login" ".login-form" "[data-testid='login-button']"; do
  echo "检查 $selector:"
  agent-browser eval "document.querySelector('$selector') ? '找到' : '未找到'" 2>&1
done

echo "---"

# 4. 检查页面URL
echo "当前页面URL:"
agent-browser eval "window.location.href" 2>&1

echo "---"

echo "检查完成"