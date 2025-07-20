import asyncio
import json
import logging
import os
from typing import List, Dict, Any
from pathlib import Path
import httpx
from openai import OpenAI
from fastmcp import Client
from dotenv import load_dotenv


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPClient:
    """
    函数名称：MCPClient
    功能描述：MCP客户端，负责连接MCP服务器并执行工具调用
    参数说明：无构造参数
    返回值：MCPClient实例
    """
    
    def __init__(self):
        self.client = None
        self.server_url = None
        
    async def connect_to_server(self, server_url: str):
        """
        函数名称：connect_to_server
        功能描述：连接到FastMCP服务器
        参数说明：
            - server_url：str，MCP服务器SSE地址
        返回值：无
        """
        self.server_url = server_url
        # 使用FastMCP Client连接到SSE服务器
        self.client = Client(server_url + "/sse")
        logger.info(f"Prepared FastMCP client for {server_url}")
        
    async def list_tools(self) -> List[Dict[str, Any]]:
        """
        函数名称：list_tools
        功能描述：获取MCP服务器提供的工具列表
        参数说明：无
        返回值：List[Dict]，工具列表
        """
        if not self.client:
            raise Exception("Not connected to MCP server")
            
        try:
            async with self.client as client:
                tools = await client.list_tools()
                # 转换为字典格式
                return [tool.model_dump() for tool in tools]
        except Exception as e:
            logger.error(f"Error listing tools: {e}")
            return []
            
    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        """
        函数名称：execute_tool
        功能描述：执行MCP工具
        参数说明：
            - tool_name：str，工具名称
            - arguments：Dict，工具参数
        返回值：str，执行结果
        """
        if not self.client:
            raise Exception("Not connected to MCP server")
            
        try:
            async with self.client as client:
                result = await client.call_tool(tool_name, arguments)
                if hasattr(result, 'content') and result.content:
                    return result.content[0].text if result.content else 'No result'
                else:
                    return str(result)
        except Exception as e:
            error_msg = f"Error executing tool {tool_name}: {str(e)}"
            logger.error(error_msg)
            return error_msg
            
    async def cleanup(self):
        """
        函数名称：cleanup
        功能描述：清理MCP客户端资源
        参数说明：无
        返回值：无
        """
        # FastMCP Client使用上下文管理器，无需手动清理
        logger.info("MCP client cleanup completed")


class LLMClient:
    """
    函数名称：LLMClient
    功能描述：LLM客户端，负责与大语言模型API通信
    参数说明：
        - model_name：str，模型名称
        - url：str，API地址
        - api_key：str，API密钥
    返回值：LLMClient实例
    """

    def __init__(self, model_name: str, url: str, api_key: str) -> None:
        self.model_name = model_name
        self.url = url
        self.client = OpenAI(api_key=api_key, base_url=url)

    def get_response(self, messages: List[Dict[str, str]]) -> str:
        """
        函数名称：get_response
        功能描述：发送消息给LLM并获取响应
        参数说明：
            - messages：List[Dict]，对话消息列表
        返回值：str，LLM响应内容
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error getting LLM response: {e}")
            return f"LLM调用失败: {str(e)}"


class ChatSession:
    """
    函数名称：ChatSession
    功能描述：聊天会话，处理用户输入和LLM响应，并与MCP工具交互
    参数说明：
        - llm_client：LLMClient，LLM客户端实例
        - mcp_client：MCPClient，MCP客户端实例
    返回值：ChatSession实例
    """

    def __init__(self, llm_client: LLMClient, mcp_client: MCPClient) -> None:
        self.mcp_client = mcp_client
        self.llm_client = llm_client

    async def cleanup(self) -> None:
        """
        函数名称：cleanup
        功能描述：清理MCP客户端资源
        参数说明：无
        返回值：无
        """
        try:
            await self.mcp_client.cleanup()
        except Exception as e:
            logging.warning(f"Warning during final cleanup: {e}")

    async def process_llm_response(self, llm_response: str) -> str:
        """
        函数名称：process_llm_response
        功能描述：处理LLM响应，解析工具调用并执行
        参数说明：
            - llm_response：str，LLM响应内容
        返回值：str，处理后的结果
        """
        try:
            # 尝试移除可能的markdown格式
            if llm_response.startswith('```json'):
                llm_response = llm_response.strip('```json').strip('```').strip()
            
            tool_call = json.loads(llm_response)
            if "tool" in tool_call and "arguments" in tool_call:
                # 获取可用工具列表
                tools = await self.mcp_client.list_tools()
                tool_names = [tool.get('name') for tool in tools]
                
                if tool_call["tool"] in tool_names:
                    try:
                        # 执行工具调用
                        result = await self.mcp_client.execute_tool(
                            tool_call["tool"], tool_call["arguments"]
                        )
                        return f"工具执行结果: {result}"
                    except Exception as e:
                        error_msg = f"工具执行错误: {str(e)}"
                        logger.error(error_msg)
                        return error_msg
                return f"未找到工具: {tool_call['tool']}"
            return llm_response
        except json.JSONDecodeError:
            # 如果不是JSON格式，直接返回原始响应
            return llm_response

    async def start(self, system_message: str) -> None:
        """
        函数名称：start
        功能描述：启动聊天会话的主循环
        参数说明：
            - system_message：str，系统消息
        返回值：无
        """
        messages = [{"role": "system", "content": system_message}]
        print("=== QT应用控制助手已启动 ===")
        print("可以使用以下指令:")
        print("- 登录账号 <用户名> <密码>")
        print("- 点击测试按钮") 
        print("- 查看应用状态")
        print("- 退出 (输入 quit/exit/退出)")
        print("================================")
        
        while True:
            try:
                # 获取用户输入
                user_input = input("用户: ").strip()
                if user_input.lower() in ["quit", "exit", "退出"]:
                    print('QT控制助手退出')
                    break
                    
                if not user_input:
                    continue
                    
                messages.append({"role": "user", "content": user_input})

                # 获取LLM的初始响应
                llm_response = self.llm_client.get_response(messages)
                print("助手:", llm_response)

                # 处理可能的工具调用
                result = await self.process_llm_response(llm_response)

                # 如果处理结果与原始响应不同，说明执行了工具调用，需要进一步处理
                while result != llm_response:
                    messages.append({"role": "assistant", "content": llm_response})
                    messages.append({"role": "system", "content": result})

                    # 将工具执行结果发送回LLM获取新响应
                    llm_response = self.llm_client.get_response(messages)
                    result = await self.process_llm_response(llm_response)
                    print("助手:", llm_response)

                messages.append({"role": "assistant", "content": llm_response})

            except KeyboardInterrupt:
                print('\nQT控制助手退出')
                break
            except Exception as e:
                logger.error(f"Chat session error: {e}")
                print(f"发生错误: {e}")


def load_env_config():
    """
    函数名称：load_env_config
    功能描述：加载环境变量配置
    参数说明：无
    返回值：无
    """
    # 获取当前脚本所在目录
    current_dir = Path(__file__).parent
    config_file = current_dir / "config.env"
    
    if config_file.exists():
        load_dotenv(config_file)
        logger.info(f"从 {config_file} 加载环境变量")
    else:
        logger.warning(f"配置文件 {config_file} 不存在，使用系统环境变量")


async def main():
    """
    函数名称：main
    功能描述：主函数，初始化客户端并启动聊天会话
    参数说明：无
    返回值：无
    """
    # 加载环境变量配置
    load_env_config()
    
    # 初始化MCP客户端
    mcp_client = MCPClient()
    
    # 从环境变量获取LLM配置
    model_name = os.getenv('LLM_MODEL_NAME', 'qwen-plus-latest')
    base_url = os.getenv('LLM_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
    
    # 获取API密钥，支持多个提供商
    api_key = (os.getenv('DASHSCOPE_API_KEY') or 
               os.getenv('OPENAI_API_KEY') or
               os.getenv('ZHIPUAI_API_KEY') or 
               os.getenv('DEEPSEEK_API_KEY'))
    
    if not api_key:
        print("❌ 请在config.env文件中设置API密钥 (DASHSCOPE_API_KEY, OPENAI_API_KEY, ZHIPUAI_API_KEY 或 DEEPSEEK_API_KEY)")
        return
        
    llm_client = LLMClient(
        model_name=model_name,
        api_key=api_key,
        url=base_url
    )
    
    logger.info(f"使用模型: {model_name}")
    logger.info(f"API地址: {base_url}")
    
    chat_session = ChatSession(llm_client=llm_client, mcp_client=mcp_client)
    
    try:
        # 连接到MCP服务器
        mcp_server_url = os.getenv('MCP_SERVER_URL', 'http://localhost:8000')
        logger.info(f"MCP服务器地址: {mcp_server_url}")
        await mcp_client.connect_to_server(mcp_server_url)
        
        # 获取可用工具列表并格式化为系统提示的一部分
        tools = await mcp_client.list_tools()
        tools_description = json.dumps(tools, ensure_ascii=False, indent=2)

        # QT应用控制专用系统提示词
        system_message = f'''
        你是一个QT应用程序控制助手，专门帮助用户操作QT应用程序。

        可用工具：{tools_description}

        响应规则：
        1、当用户请求执行QT操作时，返回严格符合以下格式的纯净JSON：
        {{
            "tool": "tool-name",
            "arguments": {{
                "argument-name": "value"
            }}
        }}

        2、禁止包含以下内容：
         - Markdown标记（如```json）
         - 自然语言解释前缀（如"结果："）
         - 多余的格式化符号

        3、常见指令映射：
         - "登录" 或 "登录账号" → 使用 login 工具
         - "点击测试按钮" 或 "测试" → 使用 test_button 工具  
         - "查看状态" 或 "获取状态" → 使用 get_state 工具

        4、在收到工具执行结果后：
         - 将结果转化为自然、友好的中文回应
         - 突出关键信息（如登录状态、操作结果等）
         - 如果操作成功，给出积极反馈
         - 如果操作失败，说明可能的原因

        正确示例：
        用户：登录账号wyx，密码124
        响应：{{"tool":"login","arguments":{{"account":"wyx","password":"124"}}}}

        用户：点击测试按钮
        响应：{{"tool":"test_button","arguments":{{"random_string":"test"}}}}

        错误示例：
        用户：登录
        错误响应：```json{{"tool":"login",...}}``` → 含Markdown
        '''
        
        # 启动聊天会话
        await chat_session.start(system_message)

    except Exception as e:
        logger.error(f"Main function error: {e}")
        print(f"启动失败: {e}")
    finally:
        # 确保资源被清理
        await chat_session.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
