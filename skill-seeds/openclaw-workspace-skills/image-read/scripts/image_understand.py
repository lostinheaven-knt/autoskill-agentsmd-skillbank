#!/usr/bin/env python3
"""
图像理解脚本

使用 doubao-seed-2.0-code 模型进行图像理解
注意：base_url 必须使用 coding plan 的 URL
"""

import os
import sys
import json
from openai import OpenAI

def read_image(image_url, question="请精确仔细描述一下这张图", model="doubao-seed-2.0-code"):
    """
    读取并理解图像
    
    Args:
        image_url (str): 图像的 URL
        question (str): 对图像的问题
        model (str): 使用的模型，默认为 doubao-seed-2.0-code
        
    Returns:
        dict: 包含响应和元数据的字典
    """
    
    # 检查 API Key
    api_key = os.getenv("ARK_API_KEY")
    if not api_key:
        return {
            "success": False,
            "error": "ARK_API_KEY 环境变量未设置",
            "suggestion": "请设置环境变量: export ARK_API_KEY='your-api-key'"
        }
    
    try:
        # 初始化客户端
        # 重要：base_url 必须使用 coding plan 的 URL
        client = OpenAI(
            base_url="https://ark.cn-beijing.volces.com/api/coding/v3",
            api_key=api_key,
        )
        
        # 调用 API
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            },
                        },
                        {
                            "type": "text", 
                            "text": question
                        },
                    ],
                }
            ],
        )
        
        # 提取响应
        result = {
            "success": True,
            "model": model,
            "question": question,
            "image_url": image_url,
            "response": response.choices[0].message.content,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            } if hasattr(response, 'usage') and response.usage else None
        }
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "image_url": image_url,
            "question": question
        }

def main():
    """命令行接口"""
    if len(sys.argv) < 2:
        print("用法: python image_understand.py <image_url> [question]")
        print("示例: python image_understand.py 'https://example.com/image.jpg' '这张图片是什么内容？'")
        sys.exit(1)
    
    image_url = sys.argv[1]
    question = sys.argv[2] if len(sys.argv) > 2 else "请精确仔细描述一下这张图"
    
    print(f"正在分析图像: {image_url}")
    print(f"问题: {question}")
    print("-" * 50)
    
    result = read_image(image_url, question)
    
    if result["success"]:
        print("✅ 图像理解成功！")
        print(f"模型: {result['model']}")
        print(f"响应: {result['response']}")
        
        if result["usage"]:
            print(f"\n使用情况:")
            print(f"  Prompt tokens: {result['usage']['prompt_tokens']}")
            print(f"  Completion tokens: {result['usage']['completion_tokens']}")
            print(f"  Total tokens: {result['usage']['total_tokens']}")
    else:
        print("❌ 图像理解失败！")
        print(f"错误: {result['error']}")
        if "suggestion" in result:
            print(f"建议: {result['suggestion']}")
    
    return 0 if result["success"] else 1

if __name__ == "__main__":
    sys.exit(main())