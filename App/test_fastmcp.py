#!/usr/bin/env python3
"""
Test script for FastMCP Qt Control Server
测试FastMCP Qt控制服务器的功能
"""

import asyncio
import json
import subprocess
import sys
import time
from typing import Dict, Any

async def test_qt_connection():
    """直接测试Qt应用连接"""
    print("🔍 测试Qt应用连接...")
    try:
        reader, writer = await asyncio.open_connection("localhost", 8088)
        
        # 发送测试消息
        message = {
            "id": "test_connection",
            "method": "execute",
            "params": {"command": "getstate"}
        }
        
        message_str = json.dumps(message) + '\n'
        writer.write(message_str.encode('utf-8'))
        await writer.drain()
        
        # 接收响应
        response_line = await reader.readline()
        response = json.loads(response_line.decode('utf-8').strip())
        
        writer.close()
        await writer.wait_closed()
        
        print("✅ Qt应用连接成功")
        print(f"📊 状态响应: {json.dumps(response, ensure_ascii=False, indent=2)}")
        return True
        
    except Exception as e:
        print(f"❌ Qt应用连接失败: {e}")
        print("💡 请确保Qt应用正在运行并监听8088端口")
        return False

def test_mcp_tools_manual():
    """手动测试MCP工具（通过导入模块）"""
    print("\n🛠️ 测试MCP工具功能...")
    
    try:
        # 导入MCP服务器模块
        sys.path.append('./mcp-server-qt')
        from main import login, test_button, get_state
        
        print("\n1️⃣ 测试登录工具:")
        result = login("admin", "123456")
        print(f"登录结果: {result}")
        
        print("\n2️⃣ 测试按钮工具:")
        result = test_button()
        print(f"按钮结果: {result}")
        
        print("\n3️⃣ 测试状态工具:")
        result = get_state()
        print(f"状态结果: {result}")
        
        print("\n✅ 所有工具测试完成!")
        return True
        
    except Exception as e:
        print(f"❌ 工具测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

class SimpleMCPClient:
    """简单的MCP客户端测试类"""
    
    def __init__(self, server_script: str):
        self.server_script = server_script
        self.process = None
        
    async def start_server(self):
        """启动MCP服务器进程"""
        print(f"🚀 启动MCP服务器: {self.server_script}")
        
        self.process = await asyncio.create_subprocess_exec(
            sys.executable, self.server_script,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd="./mcp-server-qt"
        )
        
        # 等待服务器启动
        await asyncio.sleep(2)
        print("✅ MCP服务器已启动")
        
    async def send_mcp_request(self, method: str, params: Dict[str, Any] = None):
        """发送MCP请求"""
        if not self.process:
            raise RuntimeError("MCP服务器未启动")
            
        request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params or {}
        }
        
        # 发送请求
        request_str = json.dumps(request) + '\n'
        self.process.stdin.write(request_str.encode())
        await self.process.stdin.drain()
        
        # 接收响应
        response_line = await self.process.stdout.readline()
        return json.loads(response_line.decode().strip())
        
    async def test_mcp_protocol(self):
        """测试MCP协议交互"""
        try:
            # 1. 初始化
            print("\n📋 测试MCP协议交互...")
            response = await self.send_mcp_request("initialize", {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "clientInfo": {"name": "test-client", "version": "1.0.0"}
            })
            print("✅ 初始化成功")
            
            # 2. 列出工具
            response = await self.send_mcp_request("tools/list")
            print("📋 可用工具:")
            if "result" in response and "tools" in response["result"]:
                for tool in response["result"]["tools"]:
                    print(f"  - {tool['name']}: {tool['description']}")
            
            # 3. 调用工具
            print("\n🔧 测试工具调用:")
            
            # 测试登录
            response = await self.send_mcp_request("tools/call", {
                "name": "login",
                "arguments": {"account": "admin", "password": "123456"}
            })
            print("登录工具测试:")
            print(f"  {json.dumps(response, ensure_ascii=False, indent=2)}")
            
            # 测试按钮
            response = await self.send_mcp_request("tools/call", {
                "name": "test_button",
                "arguments": {}
            })
            print("按钮工具测试:")
            print(f"  {json.dumps(response, ensure_ascii=False, indent=2)}")
            
            print("\n✅ MCP协议测试完成!")
            return True
            
        except Exception as e:
            print(f"❌ MCP协议测试失败: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    async def close(self):
        """关闭MCP服务器"""
        if self.process:
            self.process.terminate()
            await self.process.wait()
            print("👋 MCP服务器已关闭")

async def main():
    """主测试函数"""
    print("🧪 FastMCP Qt控制服务器 - 完整测试")
    print("=" * 60)
    
    # 1. 测试Qt应用连接
    qt_ok = await test_qt_connection()
    if not qt_ok:
        print("⚠️ Qt应用连接失败，部分测试可能无法完成")
    
    # 2. 手动测试MCP工具
    print("\n" + "=" * 60)
    tools_ok = test_mcp_tools_manual()
    
    # 3. 测试完整MCP协议（如果需要）
    # print("\n" + "=" * 60)
    # client = SimpleMCPClient("main.py")
    # try:
    #     await client.start_server()
    #     await client.test_mcp_protocol()
    # finally:
    #     await client.close()
    
    print("\n" + "=" * 60)
    print("🎉 测试总结:")
    print(f"  Qt应用连接: {'✅' if qt_ok else '❌'}")
    print(f"  MCP工具功能: {'✅' if tools_ok else '❌'}")
    
    if qt_ok and tools_ok:
        print("\n🎊 所有测试通过！FastMCP服务器可以正常使用")
        print("\n💡 使用建议:")
        print("  1. 在Cursor中配置MCP服务器")
        print("  2. 使用自然语言与AI助手对话")
        print("  3. 例如: '请帮我登录Qt应用，账号admin密码123456'")
    else:
        print("\n⚠️ 部分测试失败，请检查:")
        print("  - Qt应用是否正在运行")
        print("  - 端口8088是否可用")
        print("  - Python环境是否正确")

if __name__ == "__main__":
    asyncio.run(main()) 