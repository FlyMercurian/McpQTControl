#!/usr/bin/env python3
"""
验证MCP工具是否正确定义
"""

def verify_tools():
    """验证工具导入和定义"""
    print("🔍 验证MCP工具定义")
    print("=" * 40)
    
    try:
        from main import login, test_button, get_state
        
        print("✅ 工具导入成功:")
        print(f"  - login: {login}")
        print(f"  - test_button: {test_button}")
        print(f"  - get_state: {get_state}")
        
        # 检查函数签名
        import inspect
        
        print("\n📋 函数签名:")
        print(f"  - login: {inspect.signature(login)}")
        print(f"  - test_button: {inspect.signature(test_button)}")
        print(f"  - get_state: {inspect.signature(get_state)}")
        
        # 检查是否有装饰器
        print("\n🏷️ 装饰器信息:")
        for name, func in [("login", login), ("test_button", test_button), ("get_state", get_state)]:
            if hasattr(func, "__wrapped__"):
                print(f"  - {name}: 有装饰器")
            else:
                print(f"  - {name}: 无装饰器信息")
        
        return True
        
    except Exception as e:
        print(f"❌ 工具导入失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_mcp_server():
    """测试MCP服务器实例"""
    print("\n🚀 验证MCP服务器实例")
    print("=" * 40)
    
    try:
        from main import mcp
        print(f"✅ MCP服务器实例: {mcp}")
        print(f"   类型: {type(mcp)}")
        
        # 尝试获取可用方法
        methods = [method for method in dir(mcp) if not method.startswith('_')]
        print(f"   可用方法: {methods[:10]}...")  # 只显示前10个
        
        return True
        
    except Exception as e:
        print(f"❌ MCP服务器验证失败: {e}")
        return False

if __name__ == "__main__":
    print("🧪 MCP Qt控制服务器验证")
    print("=" * 50)
    
    tools_ok = verify_tools()
    server_ok = test_mcp_server()
    
    print("\n" + "=" * 50)
    print("📊 验证结果:")
    print(f"  工具定义: {'✅ 正常' if tools_ok else '❌ 异常'}")
    print(f"  服务器实例: {'✅ 正常' if server_ok else '❌ 异常'}")
    
    if tools_ok and server_ok:
        print("\n🎉 所有验证通过！")
        print("💡 建议:")
        print("  1. 重启Cursor以刷新MCP服务器")
        print("  2. 在Cursor中测试: '请帮我登录Qt应用，账号admin密码123456'")
    else:
        print("\n⚠️ 验证失败，请检查代码定义") 