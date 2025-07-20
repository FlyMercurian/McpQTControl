#!/usr/bin/env python3
"""
Qt TCP客户端
用于连接Qt应用的TCP服务器并发送命令
"""

import asyncio
import json
import socket
import logging
from typing import Optional, Dict, Any

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QtClient:
    """Qt应用TCP客户端"""
    
    def __init__(self, host: str = "localhost", port: int = 8088):
        self.host = host
        self.port = port
        self.reader: Optional[asyncio.StreamReader] = None
        self.writer: Optional[asyncio.StreamWriter] = None
        self.connected = False
        
    async def connect(self) -> bool:
        """连接到Qt应用"""
        try:
            self.reader, self.writer = await asyncio.open_connection(
                self.host, self.port
            )
            self.connected = True
            logger.info(f"已连接到Qt应用 {self.host}:{self.port}")
            return True
            
        except Exception as e:
            logger.error(f"连接Qt应用失败: {e}")
            self.connected = False
            return False
    
    async def disconnect(self):
        """断开连接"""
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
            self.connected = False
            logger.info("已断开Qt应用连接")
    
    async def _ensure_connection(self):
        """确保连接有效"""
        if not self.connected:
            success = await self.connect()
            if not success:
                raise ConnectionError("无法连接到Qt应用")
    
    async def send_command(self, command: str) -> Dict[str, Any]:
        """
        发送命令到Qt应用
        
        Args:
            command: 要发送的命令字符串
            
        Returns:
            Qt应用的响应字典
        """
        await self._ensure_connection()
        
        try:
            # 构造JSON-RPC消息
            message = {
                "id": f"mcp_{asyncio.get_event_loop().time()}",
                "method": "execute",
                "params": {
                    "command": command
                }
            }
            
            # 发送消息
            message_str = json.dumps(message) + '\n'
            self.writer.write(message_str.encode('utf-8'))
            await self.writer.drain()
            
            logger.debug(f"发送命令: {command}")
            
            # 接收响应
            response_line = await self.reader.readline()
            if not response_line:
                raise ConnectionError("Qt应用连接已关闭")
            
            response_str = response_line.decode('utf-8').strip()
            logger.debug(f"收到响应: {response_str}")
            
            # 解析JSON响应
            try:
                response_data = json.loads(response_str)
                return response_data
            except json.JSONDecodeError:
                # 如果不是JSON格式，返回原始文本
                return {
                    "success": True,
                    "message": response_str,
                    "data": {}
                }
                
        except Exception as e:
            logger.error(f"发送命令失败: {e}")
            # 重置连接状态
            self.connected = False
            raise
    
    async def send_login_command(self, account: str, password: str) -> Dict[str, Any]:
        """发送登录命令"""
        command = f"login:{account}:{password}"
        return await self.send_command(command)
    
    async def send_test_button_command(self) -> Dict[str, Any]:
        """发送测试按钮命令"""
        return await self.send_command("testbutton")
    
    async def send_get_state_command(self) -> Dict[str, Any]:
        """发送获取状态命令"""
        return await self.send_command("getstate")
    
    def format_response(self, response: Dict[str, Any]) -> str:
        """
        格式化响应消息为可读文本
        
        Args:
            response: Qt应用的响应字典
            
        Returns:
            格式化后的响应文本
        """
        if "result" in response:
            # 成功响应
            result = response["result"]
            success = result.get("success", False)
            message = result.get("message", "")
            data = result.get("data", {})
            
            status = "成功" if success else "失败"
            text = f"状态: {status}\n消息: {message}"
            
            if data:
                text += f"\n详细信息: {json.dumps(data, ensure_ascii=False, indent=2)}"
                
            return text
            
        elif "error" in response:
            # 错误响应
            error = response["error"]
            return f"错误: {error.get('message', '未知错误')}"
            
        else:
            # 其他格式响应
            return f"响应: {json.dumps(response, ensure_ascii=False, indent=2)}"

# 测试函数
async def test_qt_client():
    """测试Qt客户端功能"""
    client = QtClient()
    
    try:
        # 连接
        if not await client.connect():
            print("连接失败")
            return
        
        # 测试命令
        print("=== 测试获取状态 ===")
        response = await client.send_get_state_command()
        print(client.format_response(response))
        
        print("\n=== 测试登录 ===")
        response = await client.send_login_command("admin", "123456")
        print(client.format_response(response))
        
        print("\n=== 测试按钮 ===")
        response = await client.send_test_button_command()
        print(client.format_response(response))
        
    except Exception as e:
        print(f"测试失败: {e}")
    finally:
        await client.disconnect()

if __name__ == "__main__":
    # 运行测试
    asyncio.run(test_qt_client()) 