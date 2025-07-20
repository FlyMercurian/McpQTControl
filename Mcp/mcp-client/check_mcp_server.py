#!/usr/bin/env python3
"""
快速检查MCP服务器状态
"""
import asyncio
import httpx
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

async def check_mcp_server():
    """检查MCP服务器状态"""
    print("🔍 检查MCP服务器状态...")
    
    server_url = "http://localhost:8000"
    
    try:
        async with httpx.AsyncClient() as client:
            # 测试基本连接
            response = await client.get(f"{server_url}/", timeout=3.0)
            if response.status_code in [200, 404, 405]:
                print(f"✅ MCP服务器运行正常 (端口8000)")
                print(f"   响应状态码: {response.status_code}")
                
                # 测试工具列表
                try:
                    from main import MCPClient
                    mcp_client = MCPClient()
                    await mcp_client.connect_to_server(server_url)
                    
                    tools = await mcp_client.list_tools()
                    print(f"✅ MCP工具列表获取成功")
                    for tool in tools:
                        print(f"   🔧 {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')}")
                    
                    return True
                    
                except Exception as e:
                    print(f"⚠️ MCP工具列表获取失败: {e}")
                    return False
                    
            else:
                print(f"❌ MCP服务器响应异常: {response.status_code}")
                return False
                
    except httpx.ConnectError:
        print("❌ MCP服务器未运行 (连接被拒绝)")
        print("💡 请先启动MCP服务器:")
        print("   cd ../mcp-server-qt")
        print("   python main.py")
        return False
        
    except Exception as e:
        print(f"❌ MCP服务器检查失败: {e}")
        return False

if __name__ == "__main__":
    try:
        result = asyncio.run(check_mcp_server())
        if result:
            print("\n🎉 MCP服务器运行正常，可以进行语音控制！")
        else:
            print("\n⚠️ MCP服务器有问题，请检查并重启")
        sys.exit(0 if result else 1)
    except KeyboardInterrupt:
        print("\n🛑 检查被用户中断")
        sys.exit(0) 