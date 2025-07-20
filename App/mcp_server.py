#!/usr/bin/env python3
"""
MCP服务器 - Qt控制应用
连接MCP客户端和Qt应用的中间层服务器
"""

import asyncio
import json
import sys
from typing import Any, Dict, List, Optional

# MCP导入
try:
    from mcp.server import Server, NotificationOptions
    from mcp.server.models import InitializationOptions
    import mcp.server.stdio
    import mcp.types as types
except ImportError as e:
    print(f"MCP库导入失败: {e}", file=sys.stderr)
    print("请安装MCP库: pip install mcp", file=sys.stderr)
    sys.exit(1)

from qt_client import QtClient

class McpQtServer:
    """MCP Qt控制服务器"""
    
    def __init__(self):
        self.server = Server("mcp-qt-control")
        self.qt_client = QtClient()
        
        # 设置工具处理器
        self._setup_tools()
        
    def _setup_tools(self):
        """设置MCP工具"""
        
        # 登录工具
        @self.server.call_tool()
        async def login(arguments: dict) -> list[types.TextContent]:
            """
            登录到Qt应用
            
            Args:
                arguments: {"account": "用户名", "password": "密码"}
            """
            account = arguments.get("account", "")
            password = arguments.get("password", "")
            
            if not account or not password:
                return [types.TextContent(
                    type="text",
                    text="错误：账号和密码都是必需的"
                )]
            
            try:
                # 发送命令到Qt应用
                command = f"login:{account}:{password}"
                response = await self.qt_client.send_command(command)
                
                return [types.TextContent(
                    type="text", 
                    text=f"登录结果：{response}"
                )]
                
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=f"登录失败：{str(e)}"
                )]
        
        # 测试按钮工具  
        @self.server.call_tool()
        async def test_button(arguments: dict) -> list[types.TextContent]:
            """
            点击Qt应用的测试按钮
            """
            try:
                response = await self.qt_client.send_command("testbutton")
                
                return [types.TextContent(
                    type="text",
                    text=f"测试按钮结果：{response}"
                )]
                
            except Exception as e:
                return [types.TextContent(
                    type="text", 
                    text=f"测试按钮失败：{str(e)}"
                )]
        
        # 获取状态工具
        @self.server.call_tool()
        async def get_state(arguments: dict) -> list[types.TextContent]:
            """
            获取Qt应用当前状态
            """
            try:
                response = await self.qt_client.send_command("getstate")
                
                return [types.TextContent(
                    type="text",
                    text=f"应用状态：{response}"
                )]
                
            except Exception as e:
                return [types.TextContent(
                    type="text",
                    text=f"获取状态失败：{str(e)}"
                )]
    
    async def run(self):
        """运行MCP服务器"""
        # 初始化Qt客户端连接
        await self.qt_client.connect()
        
        # 运行MCP服务器
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream, 
                InitializationOptions(
                    server_name="mcp-qt-control",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    )
                )
            )

def main():
    """主函数"""
    server = McpQtServer()
    
    # 设置工具列表
    @server.server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        """返回可用工具列表"""
        return [
            types.Tool(
                name="login",
                description="登录到Qt应用",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "account": {
                            "type": "string",
                            "description": "用户账号"
                        },
                        "password": {
                            "type": "string", 
                            "description": "用户密码"
                        }
                    },
                    "required": ["account", "password"]
                }
            ),
            types.Tool(
                name="test_button",
                description="点击Qt应用的测试按钮",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            ),
            types.Tool(
                name="get_state",
                description="获取Qt应用当前状态",
                inputSchema={
                    "type": "object",
                    "properties": {}
                }
            )
        ]
    
    # 运行服务器
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        print("MCP服务器已停止", file=sys.stderr)
    except Exception as e:
        print(f"服务器错误: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 