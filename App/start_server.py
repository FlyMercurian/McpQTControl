#!/usr/bin/env python3
"""
MCP Qt控制服务器启动脚本
用于启动MCP服务器并提供调试信息
"""

import asyncio
import sys
import logging
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from qt_client import QtClient
from mcp_server import main

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stderr)
    ]
)

logger = logging.getLogger(__name__)

async def check_qt_connection():
    """检查Qt应用连接"""
    logger.info("检查Qt应用连接...")
    
    client = QtClient()
    try:
        if await client.connect():
            logger.info("✅ Qt应用连接正常")
            
            # 测试获取状态
            response = await client.send_get_state_command()
            logger.info("✅ Qt应用响应正常")
            logger.debug(f"状态响应: {client.format_response(response)}")
            
            return True
        else:
            logger.error("❌ 无法连接到Qt应用")
            return False
            
    except Exception as e:
        logger.error(f"❌ Qt应用连接测试失败: {e}")
        return False
    finally:
        await client.disconnect()

def print_banner():
    """打印启动横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    MCP Qt控制服务器                          ║
║                                                              ║
║  📱 连接: Qt应用 (localhost:8088)                           ║
║  🔌 协议: MCP over stdio                                     ║
║  🛠️  工具: login, test_button, get_state                     ║
║                                                              ║
║  使用说明:                                                   ║
║  1. 确保Qt应用正在运行并监听8088端口                         ║
║  2. 配置MCP客户端连接到此服务器                              ║
║  3. 使用MCP工具调用Qt应用功能                                ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner, file=sys.stderr)

async def startup_check():
    """启动检查"""
    print_banner()
    
    logger.info("正在进行启动检查...")
    
    # 检查Qt连接
    if not await check_qt_connection():
        logger.error("启动检查失败：无法连接到Qt应用")
        logger.error("请确保:")
        logger.error("  1. Qt应用正在运行")
        logger.error("  2. Qt应用监听端口8088")
        logger.error("  3. 网络连接正常")
        sys.exit(1)
    
    logger.info("🚀 启动检查完成，正在启动MCP服务器...")

if __name__ == "__main__":
    try:
        # 运行启动检查
        asyncio.run(startup_check())
        
        # 启动MCP服务器
        main()
        
    except KeyboardInterrupt:
        logger.info("服务器已停止")
    except Exception as e:
        logger.error(f"服务器启动失败: {e}")
        sys.exit(1) 