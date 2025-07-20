#!/usr/bin/env python3
"""
测试FastMCP工具注册情况
"""

import sys
import json
from main import mcp

def list_mcp_tools():
    """列出所有注册的MCP工具"""
    print("🛠️ 检查FastMCP工具注册情况:")
    print("=" * 50)
    
    # 获取注册的工具
    tools = mcp.get_tools()
    
    print(f"📋 发现 {len(tools)} 个工具:")
    for i, tool in enumerate(tools, 1):
        print(f"  {i}. {tool.name}")
        print(f"     描述: {tool.description}")
        print(f"     参数: {list(tool.inputSchema.get('properties', {}).keys())}")
        print()
    
    return tools

def test_login_tool():
    """专门测试login工具"""
    print("\n🔐 专门检查login工具:")
    print("=" * 50)
    
    tools = mcp.get_tools()
    login_tools = [t for t in tools if t.name == 'login']
    
    if login_tools:
        login_tool = login_tools[0]
        print("✅ login工具已注册")
        print(f"   名称: {login_tool.name}")
        print(f"   描述: {login_tool.description}")
        print(f"   输入参数: {json.dumps(login_tool.inputSchema, ensure_ascii=False, indent=2)}")
    else:
        print("❌ login工具未找到")
        
        # 检查是否有类似名称的工具
        all_names = [t.name for t in tools]
        print(f"   当前注册的工具: {all_names}")

if __name__ == "__main__":
    print("🔍 FastMCP Qt控制服务器工具诊断")
    print("=" * 60)
    
    try:
        # 列出工具
        tools = list_mcp_tools()
        
        # 测试login工具
        test_login_tool()
        
        print("\n" + "=" * 60)
        print("🎯 诊断总结:")
        print(f"  总工具数: {len(tools)}")
        print(f"  工具列表: {[t.name for t in tools]}")
        
        # 如果login工具缺失，给出修复建议
        if not any(t.name == 'login' for t in tools):
            print("\n⚠️ 问题发现: login工具未注册")
            print("💡 可能原因:")
            print("  1. async函数定义导致注册失败")
            print("  2. FastMCP版本兼容性问题")
            print("  3. 装饰器问题")
            print("\n🔧 修复建议:")
            print("  重新定义login工具为同步函数")
        else:
            print("\n✅ 所有工具注册正常")
            
    except Exception as e:
        print(f"❌ 诊断失败: {e}")
        import traceback
        traceback.print_exc() 