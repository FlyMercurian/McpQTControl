#!/usr/bin/env python3
"""
直接测试MCP Qt控制工具
Direct test for MCP Qt Control Tools
"""

import asyncio
import json
import sys
import os

# 添加mcp-server-qt目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mcp-server-qt'))

async def test_qt_connection():
    """测试Qt应用连接"""
    print("🔍 测试Qt应用连接...")
    try:
        reader, writer = await asyncio.open_connection("localhost", 8088)
        
        message = {
            "id": "test",
            "method": "execute",
            "params": {"command": "getstate"}
        }
        
        writer.write((json.dumps(message) + '\n').encode())
        await writer.drain()
        
        response = await reader.readline()
        result = json.loads(response.decode().strip())
        
        writer.close()
        await writer.wait_closed()
        
        print("✅ Qt应用连接成功")
        return True
        
    except Exception as e:
        print(f"❌ Qt连接失败: {e}")
        return False

async def test_mcp_tools():
    """测试MCP工具功能"""
    print("\n🛠️ 测试MCP工具...")
    
    try:
        # 导入MCP工具
        from main import login, test_button, get_state
        
        # 测试状态查询
        print("1️⃣ 测试状态查询:")
        result = await get_state()
        print(f"   {result}")
        
        # 测试登录
        print("\n2️⃣ 测试登录功能:")
        result = await login("admin", "123456")
        print(f"   {result}")
        
        # 测试按钮
        print("\n3️⃣ 测试按钮功能:")
        result = await test_button()
        print(f"   {result}")
        
        print("\n✅ MCP工具测试完成！")
        return True
        
    except Exception as e:
        print(f"❌ MCP工具测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_cursor_config():
    """显示Cursor配置"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mcp_path = os.path.join(current_dir, "mcp-server-qt", "main.py")
    
    print("\n📋 Cursor MCP配置:")
    print("=" * 50)
    print("在Cursor设置中添加以下配置:")
    print()
    print("{")
    print('  "cursor.mcpServers": {')
    print('    "qt-control": {')
    print('      "command": "python",')
    print(f'      "args": ["{mcp_path.replace(os.sep, os.sep + os.sep)}"]')
    print('    }')
    print('  }')
    print("}")
    print()
    print("配置文件位置:")
    print("- Windows: %APPDATA%\\Cursor\\User\\settings.json")
    print("- macOS: ~/Library/Application Support/Cursor/User/settings.json")
    print("- Linux: ~/.config/Cursor/User/settings.json")

async def main():
    """主测试函数"""
    print("🧪 MCP Qt控制工具测试")
    print("=" * 50)
    
    # 测试Qt连接
    qt_ok = await test_qt_connection()
    
    # 测试MCP工具
    if qt_ok:
        mcp_ok = await test_mcp_tools()
    else:
        print("⚠️ Qt应用未连接，跳过MCP工具测试")
        mcp_ok = False
    
    # 显示结果
    print("\n" + "=" * 50)
    print("🎉 测试结果:")
    print(f"  Qt应用连接: {'✅' if qt_ok else '❌'}")
    print(f"  MCP工具功能: {'✅' if mcp_ok else '❌'}")
    
    if qt_ok and mcp_ok:
        print("\n🎊 测试通过！可以在Cursor中使用MCP工具")
        show_cursor_config()
        
        print("\n💡 使用示例:")
        print("在Cursor中与AI对话:")
        print("- 请帮我登录Qt应用，账号是admin，密码是123456")
        print("- 请点击测试按钮")
        print("- 请查看Qt应用的状态")
        
    else:
        print("\n⚠️ 测试失败，请检查:")
        if not qt_ok:
            print("  - Qt应用是否正在运行")
            print("  - 端口8088是否可用")
        if not mcp_ok:
            print("  - Python环境和模块导入")
            print("  - FastMCP依赖是否安装")

if __name__ == "__main__":
    asyncio.run(main()) 