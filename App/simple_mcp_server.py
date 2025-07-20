#!/usr/bin/env python3
"""
简化版MCP服务器 - Qt控制应用
直接使用JSON-RPC协议，避免复杂的MCP库依赖
"""

import asyncio
import json
import sys
import logging
from typing import Any, Dict, List, Optional
from qt_client import QtClient

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleMcpServer:
    """简化版MCP服务器"""
    
    def __init__(self):
        self.qt_client = QtClient()
        self.request_id_counter = 1
        
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """处理MCP请求"""
        try:
            method = request.get("method", "")
            params = request.get("params", {})
            request_id = request.get("id", self.request_id_counter)
            self.request_id_counter += 1
            
            logger.info(f"处理请求: {method}")
            
            if method == "initialize":
                return await self.handle_initialize(request_id, params)
            elif method == "tools/list":
                return await self.handle_list_tools(request_id)
            elif method == "tools/call":
                return await self.handle_call_tool(request_id, params)
            else:
                return self.error_response(request_id, f"未知方法: {method}")
                
        except Exception as e:
            logger.error(f"请求处理失败: {e}")
            return self.error_response(request.get("id", 0), str(e))
    
    async def handle_initialize(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """处理初始化请求"""
        logger.info("初始化MCP连接")
        
        # 连接Qt应用
        if not await self.qt_client.connect():
            return self.error_response(request_id, "无法连接到Qt应用")
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "mcp-qt-control",
                    "version": "1.0.0"
                }
            }
        }
    
    async def handle_list_tools(self, request_id: Any) -> Dict[str, Any]:
        """返回可用工具列表"""
        tools = [
            {
                "name": "login",
                "description": "登录到Qt应用",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "account": {"type": "string", "description": "用户账号"},
                        "password": {"type": "string", "description": "用户密码"}
                    },
                    "required": ["account", "password"]
                }
            },
            {
                "name": "test_button",
                "description": "点击Qt应用的测试按钮",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            },
            {
                "name": "get_state",
                "description": "获取Qt应用当前状态",
                "inputSchema": {
                    "type": "object", 
                    "properties": {}
                }
            }
        ]
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"tools": tools}
        }
    
    async def handle_call_tool(self, request_id: Any, params: Dict[str, Any]) -> Dict[str, Any]:
        """调用工具"""
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})
        
        logger.info(f"调用工具: {tool_name}")
        
        try:
            if tool_name == "login":
                account = arguments.get("account", "")
                password = arguments.get("password", "")
                
                if not account or not password:
                    return self.error_response(request_id, "账号和密码都是必需的")
                
                response = await self.qt_client.send_login_command(account, password)
                result_text = self.qt_client.format_response(response)
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"登录结果：\n{result_text}"
                            }
                        ]
                    }
                }
                
            elif tool_name == "test_button":
                response = await self.qt_client.send_test_button_command()
                result_text = self.qt_client.format_response(response)
                
                return {
                    "jsonrpc": "2.0", 
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": f"测试按钮结果：\n{result_text}"
                            }
                        ]
                    }
                }
                
            elif tool_name == "get_state":
                response = await self.qt_client.send_get_state_command()
                result_text = self.qt_client.format_response(response)
                
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text", 
                                "text": f"应用状态：\n{result_text}"
                            }
                        ]
                    }
                }
            else:
                return self.error_response(request_id, f"未知工具: {tool_name}")
                
        except Exception as e:
            logger.error(f"工具调用失败: {e}")
            return self.error_response(request_id, f"工具调用失败: {str(e)}")
    
    def error_response(self, request_id: Any, message: str) -> Dict[str, Any]:
        """生成错误响应"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -1,
                "message": message
            }
        }
    
    async def run(self):
        """运行MCP服务器"""
        logger.info("启动简化版MCP服务器")
        
        try:
            while True:
                # 从stdin读取请求
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                
                if not line:
                    break
                    
                try:
                    request = json.loads(line.strip())
                    response = await self.handle_request(request)
                    
                    # 写入响应到stdout
                    print(json.dumps(response), flush=True)
                    
                except json.JSONDecodeError as e:
                    logger.error(f"JSON解析错误: {e}")
                    error_resp = self.error_response(0, f"JSON解析错误: {str(e)}")
                    print(json.dumps(error_resp), flush=True)
                    
        except KeyboardInterrupt:
            logger.info("服务器停止")
        finally:
            await self.qt_client.disconnect()

async def main():
    """主函数"""
    server = SimpleMcpServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main()) 