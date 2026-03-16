#!/usr/bin/env python3
"""
多图参考图像生成脚本

支持多个参考图，用于生成融合图片
例如：参考人物A的照片 + 人物B的照片，生成两人合照
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
        str: Base64 data URL
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
        print(f"读取文件失败 {file_path}: {e}")
        return None


def get_api_key():
    """
    获取 API Key
    
    优先级：
    1. MODEL_IMAGE_API_KEY 环境变量
    2. ARK_API_KEY 环境变量
    3. VOLCENGINE_ACCESS_KEY + VOLCENGINE_SECRET_KEY（自动获取）
    """
    # 1. 尝试 MODEL_IMAGE_API_KEY
    api_key = os.getenv("MODEL_IMAGE_API_KEY")
    if api_key:
        return api_key
    
    # 2. 尝试 ARK_API_KEY
    api_key = os.getenv("ARK_API_KEY")
    if api_key:
        return api_key
    
    # 3. 尝试使用火山引擎 AK/SK 获取
    access_key = os.getenv("VOLCENGINE_ACCESS_KEY")
    secret_key = os.getenv("VOLCENGINE_SECRET_KEY")
    
    if access_key and secret_key:
        try:
            # 这里可以添加自动获取逻辑
            print("警告: 需要手动设置 ARK_API_KEY 环境变量")
            print("请从火山引擎控制台获取: https://console.volcengine.com/ark/region:ark+cn-beijing/apikey")
        except:
            pass
    
    print("错误: 未找到 API Key")
    print("请设置环境变量: export ARK_API_KEY='your-api-key'")
    return None


def generate_with_multiple_references(prompt, image_paths, model=DEFAULT_MODEL, size="2K"):
    """
    使用多个参考图生成图片
    
    Args:
        prompt: 生成提示词
        image_paths: 参考图路径列表
        model: 模型名称
        size: 图片尺寸
        
    Returns:
        str: 生成的图片URL，失败返回None
    """
    # 获取 API Key
    api_key = get_api_key()
    if not api_key:
        return None
    
    # 初始化客户端
    client = Ark(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key=api_key,
    )
    
    # 处理参考图
    image_urls = []
    for i, image_path in enumerate(image_paths):
        print(f"处理参考图 {i+1}: {image_path}")
        
        # 检查是URL还是本地文件
        if image_path.startswith(('http://', 'https://')):
            # 网络URL
            image_urls.append(image_path)
            print(f"  使用网络URL")
        elif os.path.exists(image_path):
            # 本地文件，转换为base64
            data_url = read_file_as_base64(image_path)
            if data_url:
                image_urls.append(data_url)
                print(f"  转换为base64 (长度: {len(data_url)}字符)")
            else:
                print(f"  错误: 无法读取文件")
                return None
        elif image_path.startswith('data:image/'):
            # 已经是base64 data URL
            image_urls.append(image_path)
            print(f"  使用base64 data URL")
        else:
            print(f"  错误: 无法识别的图片格式 {image_path}")
            return None
    
    if not image_urls:
        print("错误: 没有有效的参考图")
        return None
    
    print(f"\n提示词: {prompt}")
    print(f"模型: {model}")
    print(f"参考图数量: {len(image_urls)}")
    print(f"尺寸: {size}")
    
    try:
        # 调用API
        print("\n正在调用多图融合API...")
        start_time = time.time()
        
        response = client.images.generate(
            model=model,
            prompt=prompt,
            image=image_urls,
            size=size,
            sequential_image_generation="disabled",
            response_format="url",
            watermark=False
        )
        
        elapsed_time = time.time() - start_time
        print(f"API调用完成，耗时: {elapsed_time:.1f}秒")
        
        # 检查响应
        if hasattr(response, 'data') and len(response.data) > 0:
            result_url = response.data[0].url
            print(f"\n✅ 生成成功!")
            print(f"生成的图片URL: {result_url}")
            return result_url
        else:
            print("错误: API响应中没有数据")
            return None
            
    except Exception as e:
        print(f"API调用失败: {e}")
        import traceback
        traceback.print_exc()
        return None


def download_image(image_url, output_path):
    """
    下载图片到本地
    
    Args:
        image_url: 图片URL
        output_path: 输出路径
        
    Returns:
        bool: 是否成功
    """
    try:
        print(f"下载图片到: {output_path}")
        urllib.request.urlretrieve(image_url, output_path)
        
        # 检查文件大小
        file_size = os.path.getsize(output_path)
        print(f"下载完成，文件大小: {file_size / 1024:.1f} KB")
        return True
        
    except Exception as e:
        print(f"下载失败: {e}")
        return False


def main():
    """命令行接口"""
    if len(sys.argv) < 3:
        print("用法: python image_generate_multi_ref.py \"<prompt>\" <image1> [image2 ...]")
        print("")
        print("示例:")
        print("  # 使用两个本地文件")
        print('  python image_generate_multi_ref.py "两人在海边合照" /path/to/person1.jpg /path/to/person2.jpg')
        print("")
        print("  # 使用网络URL")
        print('  python image_generate_multi_ref.py "融合风格" https://example.com/img1.jpg https://example.com/img2.jpg')
        print("")
        print("  # 使用base64 data URL")
        print('  python image_generate_multi_ref.py "生成图片" "data:image/jpeg;base64,..." "data:image/png;base64,..."')
        print("")
        print("参数说明:")
        print("  <prompt>: 生成提示词")
        print("  <imageN>: 参考图路径，可以是:")
        print("    - 本地文件路径")
        print("    - 网络URL (http:// 或 https://)")
        print("    - base64 data URL (data:image/...)")
        sys.exit(1)
    
    prompt = sys.argv[1]
    image_paths = sys.argv[2:]
    
    print("="*60)
    print("多图参考图像生成")
    print("="*60)
    
    # 生成图片
    result_url = generate_with_multiple_references(
        prompt=prompt,
        image_paths=image_paths,
        model=DEFAULT_MODEL,
        size="2K"
    )
    
    if result_url:
        # 自动下载图片
        timestamp = int(time.time())
        output_file = f"generated_multi_ref_{timestamp}.jpg"
        success = download_image(result_url, output_file)
        
        if success:
            print(f"\n✅ 图片已保存到: {os.path.abspath(output_file)}")
        else:
            print(f"\n⚠️  图片URL: {result_url}")
            print("   请手动下载")
    else:
        print("\n❌ 生成失败")
        sys.exit(1)


if __name__ == "__main__":
    main()