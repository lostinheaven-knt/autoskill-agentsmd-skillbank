#!/usr/bin/env python3
"""
视频理解脚本

使用 doubao-seed-2.0-code 模型进行视频理解
注意：base_url 必须使用 coding plan 的 URL
SDK: volcenginesdkarkruntime (不是 openai)
"""

import os
import sys
import json
from volcenginesdkarkruntime import Ark

def read_video(video_url, question="视频中有什么内容？", model="doubao-seed-2.0-code", fps=2):
    """
    读取并理解视频
    
    Args:
        video_url (str): 视频的 URL
        question (str): 对视频的问题
        model (str): 使用的模型，默认为 doubao-seed-2.0-code
        fps (int): 视频帧率，默认为 2
        
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
        client = Ark(
            base_url="https://ark.cn-beijing.volces.com/api/coding/v3",
            api_key=api_key,
        )
        
        # 调用 API
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "video_url",
                            "video_url": {
                                "url": video_url,
                                "fps": fps,
                            }
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
            "video_url": video_url,
            "fps": fps,
            "response": completion.choices[0].message.content,
            "usage": {
                "prompt_tokens": completion.usage.prompt_tokens,
                "completion_tokens": completion.usage.completion_tokens,
                "total_tokens": completion.usage.total_tokens
            } if hasattr(completion, 'usage') and completion.usage else None
        }
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "video_url": video_url,
            "question": question,
            "fps": fps
        }

def main():
    """命令行接口"""
    if len(sys.argv) < 2:
        print("用法: python video_understand.py <video_url> [question] [fps]")
        print("示例: python video_understand.py 'https://example.com/video.mp4' '视频中有什么内容？' 2")
        print("示例: python video_understand.py 'https://example.com/video.mp4' '请描述视频内容'")
        sys.exit(1)
    
    video_url = sys.argv[1]
    question = sys.argv[2] if len(sys.argv) > 2 else "视频中有什么内容？"
    fps = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    
    print(f"正在分析视频: {video_url}")
    print(f"问题: {question}")
    print(f"FPS: {fps}")
    print("-" * 50)
    
    result = read_video(video_url, question, fps=fps)
    
    if result["success"]:
        print("✅ 视频理解成功！")
        print(f"模型: {result['model']}")
        print(f"响应: {result['response']}")
        
        if result["usage"]:
            print(f"\n使用情况:")
            print(f"  Prompt tokens: {result['usage']['prompt_tokens']}")
            print(f"  Completion tokens: {result['usage']['completion_tokens']}")
            print(f"  Total tokens: {result['usage']['total_tokens']}")
    else:
        print("❌ 视频理解失败！")
        print(f"错误: {result['error']}")
        if "suggestion" in result:
            print(f"建议: {result['suggestion']}")
    
    return 0 if result["success"] else 1

if __name__ == "__main__":
    sys.exit(main())