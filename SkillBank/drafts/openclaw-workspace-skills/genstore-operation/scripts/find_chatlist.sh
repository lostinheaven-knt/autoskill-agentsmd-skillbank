#!/bin/bash
# 寻找Chat List入口

echo "===== 寻找Chat List入口 ====="

# 1. 检查页面是否有Chat相关元素
echo "检查Chat相关文本..."
agent-browser eval "
  const elements = document.querySelectorAll('*');
  let chatElements = [];
  elements.forEach(el => {
    if (el.textContent && el.textContent.toLowerCase().includes('chat')) {
      chatElements.push({
        tag: el.tagName,
        text: el.textContent.trim().substring(0, 50),
        id: el.id || '',
        className: el.className || ''
      });
    }
  });
  chatElements.length > 0 ? JSON.stringify(chatElements.slice(0, 5), null, 2) : '未找到包含Chat文本的元素'
" 2>&1

echo "---"

# 2. 检查AI或Assistant相关文本
echo "检查AI/Assistant相关文本..."
agent-browser eval "
  const elements = document.querySelectorAll('*');
  let aiElements = [];
  const keywords = ['ai', 'assistant', 'lui', '对话', 'chat'];
  elements.forEach(el => {
    const text = el.textContent ? el.textContent.toLowerCase() : '';
    if (keywords.some(keyword => text.includes(keyword))) {
      aiElements.push({
        tag: el.tagName,
        text: el.textContent.trim().substring(0, 50),
        id: el.id || '',
        className: el.className || ''
      });
    }
  });
  aiElements.length > 0 ? JSON.stringify(aiElements.slice(0, 5), null, 2) : '未找到AI相关元素'
" 2>&1

echo "---"

# 3. 检查可能的按钮或链接
echo "检查按钮和链接..."
agent-browser eval "
  const buttons = document.querySelectorAll('button, a, [role=\"button\"]');
  let chatButtons = [];
  buttons.forEach(btn => {
    const text = btn.textContent ? btn.textContent.toLowerCase() : '';
    if (text.includes('chat') || text.includes('ai') || text.includes('assistant')) {
      chatButtons.push({
        tag: btn.tagName,
        text: btn.textContent.trim(),
        id: btn.id || '',
        className: btn.className || ''
      });
    }
  });
  chatButtons.length > 0 ? JSON.stringify(chatButtons, null, 2) : '未找到Chat相关按钮'
" 2>&1

echo "---"

# 4. 检查侧边栏或导航
echo "检查导航菜单..."
agent-browser eval "
  // 检查侧边栏
  const sidebars = document.querySelectorAll('[class*=\"sidebar\"], [class*=\"nav\"], [class*=\"menu\"]');
  let sidebarText = '';
  sidebars.forEach(sidebar => {
    sidebarText += sidebar.textContent.substring(0, 200) + '\\n\\n';
  });
  sidebarText || '未找到明显的侧边栏'
" 2>&1

echo "---"

echo "检查完成"