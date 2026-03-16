#!/usr/bin/env python3
"""
图像生成脚本（支持参考图）

支持两种参考图格式：
1. 公网 URL：https://example.com/image.jpg
2. Base64 编码：data:image/<格式>;base64,<编码>

注意：<图片格式> 需小写，如 data:image/png;base64,<base64_image>
"""

import os
import sys
import time
import base64
import urllib.request
from volcenginesdkarkruntime import Ark

# Default model
#DEFAULT_MODEL = "doubao-seedream-5-0-260128"
DEFAULT_MODEL = "doubao-seedream-4-5-251128"


def read_file_as_base64(file_path):
    """
    读取本地文件并转换为 Base64 编码
    
    Args:
        file_path: 本地文件路径
        
    Returns:
        str: Base64 编码字符串
    """
    try:
        with open(file_path, 'rb') as f:
            image_data = f.read()
        
        # 获取文件扩展名（格式）
        ext = os.path.splitext(file_path)[1].lower().lstrip('.')
        if ext == 'jpg':
            ext = 'jpeg'  # image/jpeg
        
        # Base64 编码
        base64_str = base64.b64encode(image_data).decode('utf-8')
        
        # 构建 data URL
        data_url = f"data:image/{ext};base64,{base64_str}"
        
        return data_url
        
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None


def image_generate_with_ref(prompt: str, image_input: str = None):
    """
    基于提示生成图像，支持参考图（URL或Base64）
    
    Args:
        prompt: 生成图像的提示词
        image_input: 参考图输入，可以是：
            - 公网 URL：https://example.com/image.jpg
            - 本地文件路径：/path/to/image.jpg
            - Base64 字符串：data:image/png;base64,...（完整格式）
            
    Returns:
        str: 生成的图像文件路径
    """
    if not prompt:
        print("Prompt is empty.")
        return None

    api_key = os.getenv("MODEL_IMAGE_API_KEY") or os.getenv("ARK_API_KEY")
    if not api_key:
        print("Error: ARK_API_KEY environment variable not set")
        return None

    try:
        client = Ark(api_key=api_key)
        
        # 构建参数
        params = {
            "model": os.getenv("MODEL_IMAGE_NAME", DEFAULT_MODEL),
            "prompt": prompt,
            "size": "2k",
        }
        
        # 处理参考图
        image_url = None
        if image_input:
            # 检查是否是 Base64 格式
            if image_input.startswith("data:image/"):
                # 已经是 Base64 格式
                image_url = image_input
                print("Using Base64 encoded reference image")
            
            # 检查是否是本地文件路径
            elif os.path.exists(image_input):
                # 本地文件，转换为 Base64
                image_url = read_file_as_base64(image_input)
                if image_url:
                    print(f"Using local file as reference: {image_input}")
                else:
                    print(f"Failed to read local file: {image_input}")
                    return None
            
            else:
                # 假设是公网 URL
                image_url = image_input
                print(f"Using public URL reference image: {image_input}")
            
            if image_url:
                params["image"] = image_url
        
        print(f"Generating image with prompt: {prompt}")
        if 'image' in params:
            print(f"Reference image type: {'Base64' if 'data:image/' in params['image'] else 'URL'}")
        
        response = client.images.generate(**params)
        
        # 创建下载目录
        download_dir = os.getenv("IMAGE_DOWNLOAD_DIR", os.path.expanduser("./"))
        if not os.path.exists(download_dir):
            try:
                os.makedirs(download_dir, exist_ok=True)
            except Exception as e:
                print(f"Failed to create directory {download_dir}: {e}")
                return None
        
        # 下载生成的图像
        for i, image in enumerate(response.data):
            try:
                timestamp = int(time.time())
                filename = f"generated_image_ref_{timestamp}_{i}.png"
                filepath = os.path.join(download_dir, filename)
                
                urllib.request.urlretrieve(image.url, filepath)
                print(f"✅ Image generated and downloaded to: {filepath}")
                
                return filepath  # 返回文件路径
                
            except Exception as e:
                print(f"Failed to download image from {image.url}: {e}")
                return None
                
    except Exception as e:
        print(f"Error generating image: {e}")
        return None


def main():
    """命令行接口"""
    if len(sys.argv) < 2:
        print("用法: python image_generate_with_ref.py <prompt> [image_input]")
        print("")
        print("参数说明:")
        print("  <prompt>: 生成图像的提示词")
        print("  [image_input]: 参考图输入，可选:")
        print("    - 公网 URL: https://example.com/image.jpg")
        print("    - 本地文件路径: /path/to/image.jpg")
        print("    - Base64 字符串: data:image/png;base64,...")
        print("")
        print("示例:")
        print("  1. 使用公网 URL:")
        print("     python image_generate_with_ref.py \"一个女生\" \"https://example.com/ref.jpg\"")
        print("")
        print("  2. 使用本地文件:")
        print("     python image_generate_with_ref.py \"睡前照片\" \"/home/user/image.jpg\"")
        print("")
        print("  3. 使用 Base64 字符串:")
        print("     python image_generate_with_ref.py \"温馨场景\" \"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==\"")
        sys.exit(1)
    
    prompt = sys.argv[1]
    image_input = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = image_generate_with_ref(prompt, image_input)
    
    if not result:
        print("❌ Failed to generate image")
        sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    main()