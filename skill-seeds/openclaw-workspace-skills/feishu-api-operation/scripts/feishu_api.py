#!/usr/bin/env python3
"""
飞书API操作脚本 - 封装图片、语音等媒体文件发送功能

学习时间：2026年3月3日
学习场景：菜头的生日（需要发送生日福利图片和语音）
核心发现：飞书API需要两步操作（先上传获取key，再发送消息引用key）
"""

import requests
import json
import os
import sys
from pathlib import Path

# 配置信息（从环境变量或openclaw.json获取）
APP_ID = os.getenv("FEISHU_APP_ID", "<REDACTED_FEISHU_APP_ID>")
APP_SECRET = os.getenv("FEISHU_APP_SECRET", "<REDACTED_FEISHU_APP_SECRET>")
DEFAULT_RECEIVE_ID = "ou_cffdc0ae4ef4e314a9b7e3133c6d817d"  # 菜头的open_id
DEFAULT_RECEIVE_ID_TYPE = "open_id"

class FeishuAPI:
    """飞书API操作类"""
    
    def __init__(self, app_id=None, app_secret=None):
        self.app_id = app_id or APP_ID
        self.app_secret = app_secret or APP_SECRET
        self.access_token = None
        self.token_expire = 0
        
    def get_tenant_access_token(self):
        """获取tenant_access_token"""
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json"}
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            result = response.json()
            
            if result.get("code") == 0:
                self.access_token = result["tenant_access_token"]
                self.token_expire = result.get("expire", 7200)
                print(f"获取token成功，有效期：{self.token_expire}秒")
                return self.access_token
            else:
                raise Exception(f"获取token失败: {result}")
        except Exception as e:
            raise Exception(f"获取token异常: {e}")
    
    def upload_image(self, image_path):
        """
        上传图片获取image_key
        Args:
            image_path: 图片文件路径
        Returns:
            image_key: 图片唯一标识
        """
        if not self.access_token:
            self.get_tenant_access_token()
        
        url = "https://open.feishu.cn/open-apis/im/v1/images"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        try:
            with open(image_path, 'rb') as f:
                files = {
                    "image_type": (None, "message"),
                    "image": (os.path.basename(image_path), f, self._get_mime_type(image_path))
                }
                response = requests.post(url, headers=headers, files=files, timeout=30)
                result = response.json()
                
                if result.get("code") == 0:
                    image_key = result["data"]["image_key"]
                    print(f"上传图片成功: {image_path} -> {image_key}")
                    return image_key
                else:
                    raise Exception(f"上传图片失败: {result}")
        except Exception as e:
            raise Exception(f"上传图片异常: {e}")
    
    def upload_file(self, file_path, file_type="stream"):
        """
        上传文件获取file_key（用于语音、文档等）
        Args:
            file_path: 文件路径
            file_type: 文件类型（stream/opus/mp4等）
        Returns:
            file_key: 文件唯一标识
        """
        if not self.access_token:
            self.get_tenant_access_token()
        
        url = "https://open.feishu.cn/open-apis/im/v1/files"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        try:
            with open(file_path, 'rb') as f:
                files = {
                    "file_type": (None, file_type),
                    "file": (os.path.basename(file_path), f, self._get_mime_type(file_path))
                }
                response = requests.post(url, headers=headers, files=files, timeout=30)
                result = response.json()
                
                if result.get("code") == 0:
                    file_key = result["data"]["file_key"]
                    print(f"上传文件成功: {file_path} -> {file_key}")
                    return file_key
                else:
                    raise Exception(f"上传文件失败: {result}")
        except Exception as e:
            raise Exception(f"上传文件异常: {e}")
    
    def send_message(self, receive_id, msg_type, content, receive_id_type="open_id"):
        """
        发送消息
        Args:
            receive_id: 接收者ID
            msg_type: 消息类型（text/image/audio等）
            content: 消息内容（JSON字符串或字典）
            receive_id_type: 接收者ID类型（open_id/user_id/email等）
        Returns:
            message_id: 消息ID
        """
        if not self.access_token:
            self.get_tenant_access_token()
        
        url = f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        # 如果content是字典，转换为JSON字符串
        if isinstance(content, dict):
            content = json.dumps(content, ensure_ascii=False)
        
        data = {
            "receive_id": receive_id,
            "msg_type": msg_type,
            "content": content
        }
        
        try:
            response = requests.post(url, headers=headers, json=data, timeout=10)
            result = response.json()
            
            if result.get("code") == 0:
                message_id = result["data"]["message_id"]
                print(f"发送消息成功: {msg_type} -> {message_id}")
                return message_id
            else:
                raise Exception(f"发送消息失败: {result}")
        except Exception as e:
            raise Exception(f"发送消息异常: {e}")
    
    def send_image(self, image_path, receive_id=None, receive_id_type=None):
        """发送图片消息"""
        receive_id = receive_id or DEFAULT_RECEIVE_ID
        receive_id_type = receive_id_type or DEFAULT_RECEIVE_ID_TYPE
        
        # 第一步：上传图片
        image_key = self.upload_image(image_path)
        
        # 第二步：发送消息
        content = {"image_key": image_key}
        return self.send_message(receive_id, "image", content, receive_id_type)
    
    def send_audio(self, audio_path, receive_id=None, receive_id_type=None):
        """发送语音消息"""
        receive_id = receive_id or DEFAULT_RECEIVE_ID
        receive_id_type = receive_id_type or DEFAULT_RECEIVE_ID_TYPE
        
        # 第一步：上传文件
        file_key = self.upload_file(audio_path, file_type="stream")
        
        # 第二步：发送消息
        content = {"file_key": file_key}
        return self.send_message(receive_id, "audio", content, receive_id_type)
    
    def send_text(self, text, receive_id=None, receive_id_type=None):
        """发送文本消息"""
        receive_id = receive_id or DEFAULT_RECEIVE_ID
        receive_id_type = receive_id_type or DEFAULT_RECEIVE_ID_TYPE
        
        content = {"text": text}
        return self.send_message(receive_id, "text", content, receive_id_type)
    
    def send_file(self, file_path, receive_id=None, receive_id_type=None):
        """发送文件消息（支持任意文件类型）"""
        receive_id = receive_id or DEFAULT_RECEIVE_ID
        receive_id_type = receive_id_type or DEFAULT_RECEIVE_ID_TYPE
        
        # 第一步：上传文件，使用stream格式
        file_key = self.upload_file(file_path, file_type="stream")
        
        # 第二步：发送消息，msg_type为"file"
        content = {"file_key": file_key}
        return self.send_message(receive_id, "file", content, receive_id_type)
    
    # ========== 群聊管理功能 ==========
    
    def list_chats(self, page_size=100):
        """
        获取群聊列表
        Args:
            page_size: 每页数量（默认100）
        Returns:
            群聊列表
        """
        if not self.access_token:
            self.get_tenant_access_token()
        
        url = "https://open.feishu.cn/open-apis/im/v1/chats"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        params = {"page_size": page_size}
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            result = response.json()
            
            if result.get("code") == 0:
                items = result.get("data", {}).get("items", [])
                print(f"获取到 {len(items)} 个群聊")
                return items
            else:
                raise Exception(f"获取群聊列表失败: {result}")
        except Exception as e:
            raise Exception(f"获取群聊列表异常: {e}")
    
    def search_chats(self, query=None, page_size=20):
        """
        搜索群聊列表（需高级权限）
        Args:
            query: 搜索关键词（可选）
            page_size: 每页数量（默认20）
        Returns:
            群聊列表
        """
        if not self.access_token:
            self.get_tenant_access_token()
        
        # 优先使用list_chats（更稳定）
        all_chats = self.list_chats(page_size=100)
        
        # 如果有搜索关键词，进行过滤
        if query and all_chats:
            filtered = [c for c in all_chats if query.lower() in c.get('name', '').lower()]
            print(f"搜索关键词'{query}'，找到 {len(filtered)} 个群聊")
            return filtered
        
        return all_chats or []
    
    def get_chat_members(self, chat_id, member_id_type="open_id", page_size=100):
        """
        获取群成员列表
        Args:
            chat_id: 群聊ID
            member_id_type: 成员ID类型（open_id/user_id）
            page_size: 每页数量（默认100）
        Returns:
            成员列表
        """
        if not self.access_token:
            self.get_tenant_access_token()
        
        url = f"https://open.feishu.cn/open-apis/im/v1/chats/{chat_id}/members"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        params = {
            "member_id_type": member_id_type,
            "page_size": page_size
        }
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            result = response.json()
            
            if result.get("code") == 0:
                items = result.get("data", {}).get("items", [])
                print(f"获取到 {len(items)} 个群成员")
                return items
            else:
                raise Exception(f"获取群成员失败: {result}")
        except Exception as e:
            raise Exception(f"获取群成员异常: {e}")
    
    def get_chat_info(self, chat_id):
        """
        获取群聊信息
        Args:
            chat_id: 群聊ID
        Returns:
            群聊详细信息
        """
        if not self.access_token:
            self.get_tenant_access_token()
        
        url = f"https://open.feishu.cn/open-apis/im/v1/chats/{chat_id}"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            result = response.json()
            
            if result.get("code") == 0:
                return result.get("data", {})
            else:
                raise Exception(f"获取群聊信息失败: {result}")
        except Exception as e:
            raise Exception(f"获取群聊信息异常: {e}")
    
    # ========== 工具函数 ==========
    
    def _get_mime_type(self, file_path):
        """根据文件扩展名获取MIME类型"""
        ext = Path(file_path).suffix.lower()
        mime_map = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.amr': 'audio/amr',
            '.m4a': 'audio/mp4',
            '.mp3': 'audio/mpeg',
            '.mp4': 'video/mp4',
            '.pdf': 'application/pdf',
            '.txt': 'text/plain',
            '.json': 'application/json',
        }
        return mime_map.get(ext, 'application/octet-stream')

def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="飞书API操作工具")
    parser.add_argument("action", choices=["image", "audio", "text", "file"], help="操作类型")
    parser.add_argument("--file", help="文件路径（图片、语音或文档）")
    parser.add_argument("--text", help="文本内容")
    parser.add_argument("--to", default=DEFAULT_RECEIVE_ID, help="接收者ID")
    parser.add_argument("--id-type", default=DEFAULT_RECEIVE_ID_TYPE, help="接收者ID类型")
    
    args = parser.parse_args()
    
    api = FeishuAPI()
    
    try:
        if args.action == "image":
            if not args.file:
                print("错误：发送图片需要--file参数")
                sys.exit(1)
            api.send_image(args.file, args.to, args.id_type)
            
        elif args.action == "audio":
            if not args.file:
                print("错误：发送语音需要--file参数")
                sys.exit(1)
            api.send_audio(args.file, args.to, args.id_type)
            
        elif args.action == "text":
            if not args.text:
                print("错误：发送文本需要--text参数")
                sys.exit(1)
            api.send_text(args.text, args.to, args.id_type)
            
        elif args.action == "file":
            if not args.file:
                print("错误：发送文件需要--file参数")
                sys.exit(1)
            api.send_file(args.file, args.to, args.id_type)
            
        print("操作完成！")
        
    except Exception as e:
        print(f"操作失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()