#!/usr/bin/env python3
"""
简单的MCP测试客户端
用于测试MCP Qt控制服务器的功能
"""

import asyncio
import json
import sys
from typing import Any, Dict

class SimpleMcpClient:
    """简单的MCP客户端实现"""
    
    def __init__(self, server_command: str, server_args: list):
        self.server_command = server_command
        self.server_args = server_args
        self.process = None
        self.request_id = 1
    
    async def start_server(self):
        """启动MCP服务器进程"""
        self.process = await asyncio.create_subprocess_exec(
            self.server_command,
            *self.server_args,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        print("🚀 MCP服务器已启动")
    
    async def send_request(self, method: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """发送MCP请求"""
        if not self.process:
            raise RuntimeError("服务器未启动")
        
        request = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": method,
            "params": params or {}
        }
        self.request_id += 1
        
        # 发送请求
        request_str = json.dumps(request) + '\n'
        self.process.stdin.write(request_str.encode())
        await self.process.stdin.drain()
        
        # 接收响应
        response_line = await self.process.stdout.readline()
        response_str = response_line.decode().strip()
        
        return json.loads(response_str)
    
    async def initialize(self):
        """初始化MCP连接"""
        response = await self.send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "clientInfo": {
                "name": "test-mcp-client",
                "version": "1.0.0"
            }
        })
        print("✅ MCP连接已初始化")
        return response
    
    async def list_tools(self):
        """列出可用工具"""
        response = await self.send_request("tools/list")
        print("📋 可用工具:")
        
        if "result" in response:
            tools = response["result"]["tools"]
            for tool in tools:
                print(f"  - {tool['name']}: {tool['description']}")
        
        return response
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]):
        """调用工具"""
        response = await self.send_request("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })
        
        print(f"🔧 调用工具: {tool_name}")
        if "result" in response:
            content = response["result"]["content"]
            for item in content:
                if item["type"] == "text":
                    print(f"📝 结果: {item['text']}")
        else:
            print(f"❌ 错误: {response.get('error', '未知错误')}")
        
        return response
    
    async def close(self):
        """关闭连接"""
        if self.process:
            self.process.stdin.close()
            await self.process.wait()
            print("👋 MCP服务器已关闭")

async def main():
    """主测试函数"""
    print("🧪 MCP Qt控制服务器测试")
    print("=" * 50)
    
    # 创建客户端
    client = SimpleMcpClient("python", ["simple_mcp_server.py"])
    
    try:
        # 启动服务器
        await client.start_server()
        await asyncio.sleep(2)  # 等待服务器启动
        
        # 初始化连接
        await client.initialize()
        
        # 列出工具
        await client.list_tools()
        
        print("\n" + "=" * 50)
        print("🎯 开始功能测试")
        
        # 测试获取状态
        print("\n1️⃣ 测试获取状态:")
        await client.call_tool("get_state", {})
        
        # 测试登录
        print("\n2️⃣ 测试登录:")
        await client.call_tool("login", {
            "account": "admin", 
            "password": "123456"
        })
        
        # 测试按钮
        print("\n3️⃣ 测试按钮:")
        await client.call_tool("test_button", {})
        
        print("\n✅ 所有测试完成!")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        await client.close()

def interactive_mode():
    """交互模式"""
    print("🎮 交互模式 - 输入命令来测试MCP服务器")
    print("可用命令:")
    print("  login <账号> <密码>  - 登录")
    print("  test                 - 点击测试按钮") 
    print("  state                - 获取状态")
    print("  quit                 - 退出")
    print("=" * 50)
    
    async def run_interactive():
        client = SimpleMcpClient("python", ["simple_mcp_server.py"])
        
        try:
            await client.start_server()
            await asyncio.sleep(2)
            await client.initialize()
            await client.list_tools()
            
            while True:
                try:
                    cmd = input("\n> ").strip().split()
                    if not cmd:
                        continue
                    
                    if cmd[0] == "quit":
                        break
                    elif cmd[0] == "login" and len(cmd) >= 3:
                        await client.call_tool("login", {
                            "account": cmd[1],
                            "password": cmd[2]
                        })
                    elif cmd[0] == "test":
                        await client.call_tool("test_button", {})
                    elif cmd[0] == "state":
                        await client.call_tool("get_state", {})
                    else:
                        print("❌ 无效命令")
                        
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"❌ 命令执行失败: {e}")
            
        finally:
            await client.close()
    
    asyncio.run(run_interactive())

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        asyncio.run(main()) 