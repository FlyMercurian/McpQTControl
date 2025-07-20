#!/usr/bin/env python3
"""
直接启动MCP客户端，跳过连接测试
用于解决FastMCP stdio模式的连接测试问题
"""

import asyncio
import sys
import os
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

async def direct_start():
    """直接启动MCP客户端主程序"""
    print("🚀 QT应用控制 MCP 客户端 - 直接启动模式")
    print("=" * 50)
    print("⚡ 跳过连接测试，直接启动客户端...")
    print()
    
    try:
        # 导入并运行主程序
        from main import main as run_main
        await run_main()
    except KeyboardInterrupt:
        print("\n用户中断，程序退出")
    except Exception as e:
        print(f"\n启动失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(direct_start())
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(0) 