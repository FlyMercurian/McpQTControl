"""
MCP Qt Control Server using FastMCP

This MCP server connects to Qt application on port 8088 and provides tools to:
- Login to the Qt application
- Click test button  
- Get application state
"""

import asyncio
import json
import socket
import logging
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP("Qt Control Server")

class QtClient:
    """Simple Qt TCP client for MCP server"""
    
    def __init__(self, host="localhost", port=8088):
        self.host = host
        self.port = port
        
    async def send_command(self, command: str) -> dict:
        """Send command to Qt application"""
        try:
            reader, writer = await asyncio.open_connection(self.host, self.port)
            
            # Construct JSON-RPC message
            message = {
                "id": f"mcp_{asyncio.get_event_loop().time()}",
                "method": "execute", 
                "params": {"command": command}
            }
            
            # Send message
            message_str = json.dumps(message) + '\n'
            writer.write(message_str.encode('utf-8'))
            await writer.drain()
            
            # Receive response
            response_line = await reader.readline()
            response_str = response_line.decode('utf-8').strip()
            
            # Close connection
            writer.close()
            await writer.wait_closed()
            
            # Parse response
            try:
                return json.loads(response_str)
            except json.JSONDecodeError:
                return {"success": True, "message": response_str}
                
        except Exception as e:
            logger.error(f"Qt connection failed: {e}")
            return {"success": False, "message": f"连接Qt应用失败: {str(e)}"}

# Create Qt client instance
qt_client = QtClient()

@mcp.tool()
def login(account: str, password: str) -> str:
    """
    Login to Qt application
    
    Args:
        account: User account name
        password: User password
        
    Returns:
        Login result message
    """
    import asyncio
    
    async def _do_login():
        command = f"login:{account}:{password}"
        response = await qt_client.send_command(command)
        return format_qt_response(response, "登录")
    
    try:
        # 尝试在现有事件循环中运行
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # 如果事件循环正在运行，创建任务
            import concurrent.futures
            import threading
            
            def run_in_thread():
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    return new_loop.run_until_complete(_do_login())
                finally:
                    new_loop.close()
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(run_in_thread)
                return future.result(timeout=30)
        else:
            return asyncio.run(_do_login())
    except Exception as e:
        logger.error(f"登录失败: {e}")
        return f"登录失败: {str(e)}"

@mcp.tool()
def test_button() -> str:
    """
    Click the test button in Qt application
    
    Returns:
        Test button click result
    """
    import asyncio
    
    async def _do_test():
        response = await qt_client.send_command("testbutton")
        return format_qt_response(response, "测试按钮")
    
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            import threading
            
            def run_in_thread():
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    return new_loop.run_until_complete(_do_test())
                finally:
                    new_loop.close()
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(run_in_thread)
                return future.result(timeout=30)
        else:
            return asyncio.run(_do_test())
    except Exception as e:
        logger.error(f"测试按钮失败: {e}")
        return f"测试按钮失败: {str(e)}"

@mcp.tool()
def get_state() -> str:
    """
    Get current state of Qt application
    
    Returns:
        Application state information
    """
    import asyncio
    
    async def _do_get_state():
        response = await qt_client.send_command("getstate")
        return format_qt_response(response, "状态查询")
    
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            import threading
            
            def run_in_thread():
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    return new_loop.run_until_complete(_do_get_state())
                finally:
                    new_loop.close()
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(run_in_thread)
                return future.result(timeout=30)
        else:
            return asyncio.run(_do_get_state())
    except Exception as e:
        logger.error(f"状态查询失败: {e}")
        return f"状态查询失败: {str(e)}"

def format_qt_response(response: dict, action: str) -> str:
    """Format Qt application response for display"""
    if "result" in response:
        # Success response
        result = response["result"]
        success = result.get("success", False)
        message = result.get("message", "")
        data = result.get("data", {})
        
        status = "✅ 成功" if success else "❌ 失败"
        text = f"{action}结果: {status}\n消息: {message}"
        
        if data:
            text += f"\n详细信息: {json.dumps(data, ensure_ascii=False, indent=2)}"
            
        return text
        
    elif "error" in response:
        # Error response
        error = response["error"]
        return f"{action}失败: {error.get('message', '未知错误')}"
        
    elif "success" in response:
        # Simple response format
        status = "✅ 成功" if response["success"] else "❌ 失败"
        message = response.get("message", "")
        return f"{action}结果: {status}\n消息: {message}"
        
    else:
        # Fallback
        return f"{action}响应: {json.dumps(response, ensure_ascii=False, indent=2)}"

# Add a resource to show server status
@mcp.resource("resource://qt-control/status")
def get_server_status() -> str:
    """Get MCP server status"""
    return """
🚀 MCP Qt控制服务器运行中

📱 连接目标: Qt应用 (localhost:8088)
🛠️ 可用工具:
  - login(account, password) - 登录到Qt应用
  - test_button() - 点击测试按钮
  - get_state() - 获取应用状态

使用方法:
- 请帮我登录Qt应用，账号是admin，密码是123456
- 请点击测试按钮
- 请查看Qt应用的当前状态
"""

# Add a prompt for better user interaction
@mcp.prompt()
def qt_control_prompt(action: str = "login") -> str:
    """Generate Qt control prompt"""
    prompts = {
        "login": "请协助用户登录Qt应用程序，需要获取账号和密码信息",
        "test": "请协助用户点击Qt应用程序的测试按钮", 
        "state": "请协助用户查看Qt应用程序的当前状态",
        "help": "请向用户介绍Qt控制服务器的功能和使用方法"
    }
    
    return prompts.get(action, prompts["help"])

if __name__ == "__main__":
    import sys
    
    # Test connection on startup
    async def test_connection():
        logger.info("测试Qt应用连接...")
        try:
            response = await qt_client.send_command("getstate")
            logger.info(f"📊 Qt应用原始响应: {response}")
            
            # 检查不同的响应格式
            if response.get("success", False):
                logger.info("✅ Qt应用连接正常")
            elif "result" in response and response["result"].get("success", False):
                logger.info("✅ Qt应用连接正常 (JSON-RPC格式)")
            else:
                logger.warning("⚠️ Qt应用连接可能有问题")
                logger.warning(f"   响应详情: {json.dumps(response, ensure_ascii=False, indent=2)}")
                
        except Exception as e:
            logger.error(f"❌ Qt应用连接失败: {e}")
    
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # 仅测试模式
        asyncio.run(test_connection())
    else:
        # MCP服务器模式
        logger.info("🚀 启动FastMCP Qt控制服务器...")
        
        # 先测试连接
        try:
            asyncio.run(test_connection())
        except Exception as e:
            logger.warning(f"初始连接测试失败: {e}")
        
        logger.info("📡 MCP服务器已准备就绪，等待Cursor连接...")
        
        # 启动MCP服务器 (FastMCP会自动处理stdin/stdout)
        mcp.run()