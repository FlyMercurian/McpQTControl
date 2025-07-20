#!/usr/bin/env python3
"""
QT应用控制 MCP 客户端 - 简单启动（跳过连接测试）
适用于已知服务器正在运行的情况
"""

import asyncio
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

def load_config():
    """加载配置文件"""
    try:
        from dotenv import load_dotenv
        current_dir = Path(__file__).parent
        config_file = current_dir / "config.env"
        
        if config_file.exists():
            load_dotenv(config_file)
            print("✅ 从 config.env 加载配置")
        else:
            print("⚠️  使用系统环境变量")
    except ImportError:
        print("⚠️  未安装python-dotenv，使用系统环境变量")

async def direct_start():
    """直接启动MCP客户端主程序"""
    print("🚀 QT应用控制 MCP 客户端 - 简单启动模式")
    print("=" * 50)
    print("⚡ 跳过连接测试，直接启动客户端...")
    
    # 加载配置
    load_config()
    
    print("\n💡 提示:")
    print("  • 请确保MCP服务器正在运行 (cd ../mcp-server-qt && python main.py)")
    print("  • 请确保Qt应用正在运行")
    print("  • 如果连接失败，请检查服务器状态")
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