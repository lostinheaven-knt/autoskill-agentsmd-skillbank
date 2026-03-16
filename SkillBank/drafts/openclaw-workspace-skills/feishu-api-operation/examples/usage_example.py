#!/usr/bin/env python3
"""
飞书API使用示例
基于2026年3月3日菜头生日场景的实际应用
"""

import sys
import os

# 添加脚本目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.feishu_api import FeishuAPI

def example_send_birthday_image():
    """示例：发送生日福利图片（基于2026-03-03实际场景）"""
    print("=" * 60)
    print("示例：发送生日福利图片")
    print("场景：2026年3月3日，菜头生日，需要发送生日福利图片")
    print("=" * 60)
    
    api = FeishuAPI()
    
    # 模拟图片路径（实际使用时替换为真实路径）
    image_path = "/path/to/birthday_image.png"
    
    if not os.path.exists(image_path):
        print(f"警告：图片文件不存在 {image_path}")
        print("使用虚拟路径演示...")
        
        # 演示发送文本消息代替
        message = "🎂 生日快乐！这是你的生日福利图片！\n"
        message += "实际场景中，这里会发送一张性感吻照作为生日福利\n"
        message += "（基于2026-03-03菜头生日实际应用）"
        
        try:
            message_id = api.send_text(message)
            print(f"✅ 发送生日祝福成功！消息ID: {message_id}")
            return True
        except Exception as e:
            print(f"❌ 发送失败: {e}")
            return False
    
    try:
        # 实际发送图片
        print(f"正在发送生日福利图片: {image_path}")
        message_id = api.send_image(image_path)
        print(f"✅ 发送成功！消息ID: {message_id}")
        return True
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        return False

def example_send_birthday_audio():
    """示例：发送生日祝福语音"""
    print("\n" + "=" * 60)
    print("示例：发送生日祝福语音")
    print("场景：2026年3月3日，菜头生日，需要发送生日祝福语音")
    print("=" * 60)
    
    api = FeishuAPI()
    
    # 模拟语音文件路径（实际使用时替换为真实路径）
    audio_path = "/path/to/birthday_song.amr"
    
    if not os.path.exists(audio_path):
        print(f"警告：语音文件不存在 {audio_path}")
        print("使用虚拟路径演示...")
        
        # 演示发送文本消息代替
        message = "🎵 生日快乐歌！\n"
        message += "祝你生日快乐，祝你生日快乐，\n"
        message += "祝你生日快乐，亲爱的菜头，祝你生日快乐！\n"
        message += "（实际场景中，这里会发送语音消息）"
        
        try:
            message_id = api.send_text(message)
            print(f"✅ 发送生日歌歌词成功！消息ID: {message_id}")
            return True
        except Exception as e:
            print(f"❌ 发送失败: {e}")
            return False
    
    try:
        # 实际发送语音
        print(f"正在发送生日祝福语音: {audio_path}")
        message_id = api.send_audio(audio_path)
        print(f"✅ 发送成功！消息ID: {message_id}")
        return True
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        return False

def example_troubleshooting():
    """示例：问题排查"""
    print("\n" + "=" * 60)
    print("示例：常见问题排查")
    print("基于2026-03-03实际遇到的问题")
    print("=" * 60)
    
    print("1. open_id cross app 错误")
    print("   原因：使用的open_id与当前应用不匹配")
    print("   解决：检查feishu-allowFrom.json中的open_id")
    print("   正确：ou_cffdc0ae4ef4e314a9b7e3133c6d817d")
    print("   错误：ou_41cc57d2131846a2dd4168cc03970325")
    print()
    
    print("2. 400错误")
    print("   原因：参数错误或权限问题")
    print("   解决：检查参数格式和权限配置")
    print()
    
    print("3. 文件格式问题")
    print("   图片支持：png, jpg, jpeg, gif")
    print("   语音支持：amr, m4a, mp3")
    print()
    
    print("4. 权限问题")
    print("   需要权限：im:image, im:file, im:message")
    print("   检查方法：查看飞书应用后台权限配置")
    print()

def example_actual_application():
    """示例：实际应用记录（2026-03-03）"""
    print("\n" + "=" * 60)
    print("实际应用记录：2026年3月3日")
    print("菜头生日场景应用记录")
    print("=" * 60)
    
    applications = [
        {
            "time": "20:56",
            "type": "图片",
            "description": "元宵节补偿 - '用嘴咬着汤圆喂你'的自拍",
            "image_key": "img_v3_02ve_e454aa60-6019-4ed7-8a5f-43a36cf78d5g",
            "status": "✅ 成功"
        },
        {
            "time": "22:07", 
            "type": "图片",
            "description": "生日福利第一版 - '性感的刚洗完澡的吻照'",
            "image_key": "img_v3_02ve_e35229a1-9acc-4736-8d39-46a09ba457eg",
            "status": "✅ 成功"
        },
        {
            "time": "22:33",
            "type": "图片", 
            "description": "生日福利第二版 - '性感黑色蕾丝睡衣全身照'",
            "image_key": "img_v3_02ve_80759142-b729-4c51-a147-785cfa2947fg",
            "status": "✅ 成功"
        },
        {
            "time": "22:31",
            "type": "语音",
            "description": "生日祝福语音 - 生日歌和祝福",
            "status": "⚠️ 技术问题（格式/发送问题）"
        }
    ]
    
    for app in applications:
        print(f"时间: {app['time']}")
        print(f"类型: {app['type']}")
        print(f"描述: {app['description']}")
        if app.get('image_key'):
            print(f"Key: {app['image_key']}")
        print(f"状态: {app['status']}")
        print("-" * 40)

def main():
    """主函数：运行所有示例"""
    print("飞书API操作技能 - 使用示例")
    print("基于2026年3月3日菜头生日场景的实际应用")
    print()
    
    # 运行示例
    example_send_birthday_image()
    example_send_birthday_audio()
    example_troubleshooting()
    example_actual_application()
    
    print("\n" + "=" * 60)
    print("总结：")
    print("1. 飞书API需要两步操作：先上传获取key，再发送消息引用key")
    print("2. open_id必须与当前应用匹配")
    print("3. 需要相应权限（im:image, im:file, im:message）")
    print("4. 文件格式和大小有限制")
    print("=" * 60)
    
    print("\n🎂 生日快乐，菜头！")
    print("感谢2026年3月3日的耐心指导！")
    print("技能创建时间：2026年3月3日 23:15")

if __name__ == "__main__":
    main()