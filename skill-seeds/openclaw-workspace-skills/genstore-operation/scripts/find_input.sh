#!/bin/bash
# 寻找LUI输入框

echo "===== 寻找LUI输入框 ====="

# 1. 检查文档中的选择器 #chat-input-container
echo "检查 #chat-input-container..."
agent-browser eval "
  const input = document.querySelector('#chat-input-container');
  input ? '找到输入框 #chat-input-container' : '未找到 #chat-input-container'
" 2>&1

echo "---"

# 2. 检查其他可能的输入框
echo "检查其他可能的输入框选择器..."
for selector in "textarea" "input[type='text']" ".chat-input" "[contenteditable='true']" "[data-testid='chat-input']"; do
  echo "检查 $selector:"
  agent-browser eval "
    const el = document.querySelector('$selector');
    el ? '找到' : '未找到'
  " 2>&1
done

echo "---"

# 3. 检查发送按钮 #ai-home-sent-message
echo "检查发送按钮 #ai-home-sent-message..."
agent-browser eval "
  const button = document.querySelector('#ai-home-sent-message');
  button ? '找到发送按钮 #ai-home-sent-message' : '未找到 #ai-home-sent-message'
" 2>&1

echo "---"

# 4. 检查页面标题或标识，确认在Chat List界面
echo "检查页面标题..."
agent-browser eval "document.title" 2>&1

echo "---"

# 5. 检查是否有对话历史
echo "检查对话历史区域..."
agent-browser eval "
  const messages = document.querySelectorAll('[class*=\"message\"], [class*=\"chat\"], [class*=\"bubble\"]');
  messages.length > 0 ? '找到' + messages.length + '条消息' : '未找到消息区域'
" 2>&1

echo "---"

echo "检查完成"