#!/usr/bin/env python3
"""
简单的MCP服务器连接测试
"""
import asyncio
import httpx

async def test_mcp_connection():
    print("🔍 测试MCP服务器连接...")
    
    try:
        async with httpx.AsyncClient() as client:
            print("1. 测试基本连接...")
            response = await client.get("http://localhost:8000", timeout=10.0)
            print(f"   基本连接响应: {response.status_code}")
            
            print("2. 测试SSE端点...")
            response = await client.get("http://localhost:8000/sse", timeout=10.0)
            print(f"   SSE端点响应: {response.status_code}")
            print(f"   响应头: {dict(response.headers)}")
            print(f"   响应内容: {response.text[:200]}...")
            
            if response.status_code == 200:
                print("✅ MCP服务器连接成功！")
                return True
            else:
                print(f"❌ 连接失败，状态码: {response.status_code}")
                return False
                
    except httpx.ConnectError as e:
        print(f"❌ 连接错误: {e}")
        print("   - 检查MCP服务器是否运行")
        print("   - 检查端口8000是否正确")
    except httpx.TimeoutException as e:
        print(f"❌ 连接超时: {e}")
        print("   - 服务器响应可能很慢")
    except Exception as e:
        print(f"❌ 其他错误: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        
    return False

if __name__ == "__main__":
    asyncio.run(test_mcp_connection()) 