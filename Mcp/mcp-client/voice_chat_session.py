"""
语音聊天会话模块
继承ChatSession，集成语音录制和语音识别功能
"""

import os
import asyncio
import logging
from pathlib import Path
from typing import Optional

from main import ChatSession, LLMClient, MCPClient
from voice_input import VoiceRecorder, KeyboardVoiceInput, AUDIO_AVAILABLE
from speech_recognizer import SpeechRecognizer, VoiceCommandProcessor, VOICE_API_AVAILABLE

logger = logging.getLogger(__name__)


class VoiceChatSession(ChatSession):
    """
    函数名称：VoiceChatSession
    功能描述：语音聊天会话，支持语音输入和文字输入两种模式
    参数说明：
        - llm_client：LLMClient，LLM客户端实例
        - mcp_client：MCPClient，MCP客户端实例
        - voice_enabled：bool，是否启用语音功能，默认True
    返回值：VoiceChatSession实例
    """
    
    def __init__(self, llm_client: LLMClient, mcp_client: MCPClient, voice_enabled: bool = True):
        super().__init__(llm_client, mcp_client)
        
        self.voice_enabled = voice_enabled and AUDIO_AVAILABLE and VOICE_API_AVAILABLE
        self.voice_recorder = None
        self.voice_input = None
        self.speech_recognizer = None
        self.voice_processor = None
        
        # 初始化语音组件
        if self.voice_enabled:
            try:
                self._initialize_voice_components()
                logger.info("语音功能已启用")
            except Exception as e:
                logger.warning(f"语音功能初始化失败: {e}")
                self.voice_enabled = False
        else:
            logger.info("语音功能已禁用")
    
    def _initialize_voice_components(self):
        """
        函数名称：_initialize_voice_components
        功能描述：初始化语音相关组件
        参数说明：无
        返回值：无
        """
        # 从环境变量获取语音配置
        sample_rate = int(os.getenv('VOICE_SAMPLE_RATE', '16000'))
        max_duration = int(os.getenv('MAX_RECORDING_DURATION', '30'))
        
        # 初始化录音器
        self.voice_recorder = VoiceRecorder(
            sample_rate=sample_rate,
            max_duration=max_duration
        )
        
        # 初始化键盘输入监听器
        self.voice_input = KeyboardVoiceInput(self.voice_recorder)
        
        # 初始化语音识别器
        voice_model = os.getenv('VOICE_MODEL', 'qwen-omni-turbo-0119')
        self.speech_recognizer = SpeechRecognizer(model_name=voice_model)
        
        # 初始化语音指令处理器
        self.voice_processor = VoiceCommandProcessor(self.speech_recognizer)
    
    async def cleanup(self) -> None:
        """
        函数名称：cleanup
        功能描述：清理语音资源和MCP客户端资源
        参数说明：无
        返回值：无
        """
        try:
            # 清理语音资源
            if self.voice_recorder:
                self.voice_recorder.cleanup()
                
            # 清理MCP资源
            await super().cleanup()
            
        except Exception as e:
            logger.warning(f"清理资源时出错: {e}")
    
    def _get_user_input(self, prompt: str = "用户") -> str:
        """
        函数名称：_get_user_input
        功能描述：获取用户输入，支持语音和文字两种模式
        参数说明：
            - prompt：输入提示符
        返回值：str，用户输入内容
        """
        if self.voice_enabled:
            # 语音+文字混合模式
            print(f"\n{prompt}> ", end="")
            print("💬 输入方式：直接输入文字 或 按 [V键] 语音输入（按一次开始，再按一次结束）")
            
            # 尝试语音输入
            audio_file = self.voice_input.wait_for_voice_input()
            
            if audio_file:
                # 有语音输入，进行识别
                return self._process_voice_input(audio_file)
            else:
                # 没有语音输入，等待文字输入
                return input(f"{prompt}> ").strip()
        else:
            # 纯文字模式
            return input(f"{prompt}> ").strip()
    
    def _process_voice_input(self, audio_file_path: str) -> str:
        """
        函数名称：_process_voice_input
        功能描述：处理语音输入，转换为文字
        参数说明：
            - audio_file_path：录音文件路径
        返回值：str，识别的文字内容
        """
        try:
            print("🔄 语音识别中，请稍候...")
            
            # 检查是否为静音（简单检查，不调用API）
            if self.speech_recognizer.is_silent_audio(audio_file_path):
                print("⚠️ 检测到静音文件，已忽略")
                return ""
            
            # 语音识别 - 使用优化的提示词
            recognized_text = self.speech_recognizer.recognize_from_file(
                audio_file_path, 
                "将音频转为简短文字指令，不要解释代码，只要用户说的话"
            )
            
            # 检查识别结果是否为空或太短
            if not recognized_text or len(recognized_text.strip()) < 2:
                print("⚠️ 语音识别结果为空或太短，已忽略")
                return ""
            
            print(f"📝 识别结果: {recognized_text}")
            
            # 确认或重录
            if self._should_auto_confirm():
                return recognized_text
            else:
                return self._confirm_voice_input(recognized_text, audio_file_path)
                
        except Exception as e:
            error_msg = f"语音识别失败: {str(e)}"
            print(f"❌ {error_msg}")
            logger.error(error_msg)
            return ""
    
    def _should_auto_confirm(self) -> bool:
        """
        函数名称：_should_auto_confirm
        功能描述：检查是否应该自动确认语音识别结果
        参数说明：无
        返回值：bool，是否自动确认
        """
        return os.getenv('AUTO_CONFIRM_VOICE', 'false').lower() == 'true'
    
    def _confirm_voice_input(self, recognized_text: str, audio_file_path: str) -> str:
        """
        函数名称：_confirm_voice_input
        功能描述：确认语音识别结果，支持重录和手动输入
        参数说明：
            - recognized_text：识别的文字
            - audio_file_path：音频文件路径
        返回值：str，最终确认的输入内容
        """
        while True:
            choice = input("✅ 确认执行此操作? (y确认/n手动输入/r重录/s跳过): ").lower().strip()
            
            if choice == 'y' or choice == '':
                return recognized_text
            elif choice == 'n':
                manual_input = input("请手动输入: ").strip()
                return manual_input
            elif choice == 'r':
                print("🎤 请重新录音...")
                audio_file = self.voice_input.wait_for_voice_input("重新录音")
                if audio_file:
                    return self._process_voice_input(audio_file)
                else:
                    print("⚠️ 重录取消")
                    continue
            elif choice == 's':
                return ""
            else:
                print("无效选择，请输入 y/n/r/s")
    
    async def start(self, system_message: str) -> None:
        """
        函数名称：start
        功能描述：启动语音聊天会话的主循环
        参数说明：
            - system_message：系统消息
        返回值：无
        """
        messages = [{"role": "system", "content": system_message}]
        
        # 打印启动信息
        print("=== QT应用语音控制助手已启动 ===")
        print("🎤 语音模式:", "✅ 已启用" if self.voice_enabled else "❌ 已禁用")
        print("💬 支持的输入方式:")
        if self.voice_enabled:
            print("  • 直接输入文字")
            print("  • 按住 [V键] 语音输入")
        else:
            print("  • 仅支持文字输入")
        print("  • 输入 'quit/exit/退出' 结束会话")
        
        print("\n📝 支持的自然语言指令:")
        print("  • 登录账号 <用户名> <密码>")
        print("  • 点击测试按钮")
        print("  • 查看应用状态")
        print("=" * 40)
        
        while True:
            try:
                # 获取用户输入（语音或文字）
                user_input = self._get_user_input("用户")
                
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
                
                # 如果处理结果与原始响应不同，说明执行了工具调用
                if result != llm_response:
                    print(f"🛠️ {result}")  # 显示工具执行结果
                    
                    # 将工具执行结果发送回LLM获取友好响应
                    messages.append({"role": "assistant", "content": llm_response})
                    messages.append({"role": "system", "content": result})
                    
                    # 获取LLM的友好响应
                    friendly_response = self.llm_client.get_response(messages)
                    print("助手:", friendly_response)
                    messages.append({"role": "assistant", "content": friendly_response})
                else:
                    # 非工具调用，直接添加到消息历史
                    messages.append({"role": "assistant", "content": llm_response})

            except KeyboardInterrupt:
                print('\nQT控制助手退出')
                break
            except Exception as e:
                logger.error(f"Voice chat session error: {e}")
                print(f"发生错误: {e}")
                
                # 语音功能出错时，可以降级到文字模式
                if self.voice_enabled and "语音" in str(e):
                    print("⚠️ 语音功能异常，已切换到文字输入模式")
                    self.voice_enabled = False


def test_voice_chat():
    """测试语音聊天功能"""
    print("🎙️ 语音聊天测试")
    print("=" * 40)
    
    try:
        # 这里只是测试组件初始化，不运行完整会话
        from main import LLMClient, MCPClient
        
        # 模拟客户端（测试用）
        class MockLLMClient:
            def get_response(self, messages):
                return "测试响应"
        
        class MockMCPClient:
            async def cleanup(self):
                pass
        
        llm_client = MockLLMClient()
        mcp_client = MockMCPClient()
        
        voice_session = VoiceChatSession(llm_client, mcp_client, voice_enabled=True)
        
        if voice_session.voice_enabled:
            print("✅ 语音聊天会话初始化成功")
            print("✅ 语音组件可用")
        else:
            print("⚠️ 语音功能不可用，将使用文字模式")
            
        # 清理资源
        asyncio.run(voice_session.cleanup())
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")


if __name__ == "__main__":
    test_voice_chat() 