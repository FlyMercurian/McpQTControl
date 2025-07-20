"""
语音识别API封装模块
集成阿里云语音识别API，支持本地音频文件转文字
"""

import os
import sys
import logging
from pathlib import Path
from typing import Optional

# 导入同目录下的语音识别模块
try:
    from .voice2text import audio_to_text_from_file, create_voice_client
    VOICE_API_AVAILABLE = True
except ImportError:
    try:
        # 如果相对导入失败，尝试直接导入
        from voice2text import audio_to_text_from_file, create_voice_client
        VOICE_API_AVAILABLE = True
    except ImportError as e:
        VOICE_API_AVAILABLE = False
        logging.warning(f"语音识别API不可用: {e}")

logger = logging.getLogger(__name__)


class SpeechRecognizer:
    """
    函数名称：SpeechRecognizer
    功能描述：语音识别器，封装阿里云语音转文字API
    参数说明：
        - model_name：语音识别模型，默认qwen-omni-turbo-0119
        - prompt：识别提示词，默认为qt控制场景优化
    返回值：SpeechRecognizer实例
    """
    
    def __init__(self, model_name: str = "qwen-omni-turbo-0119", 
                 prompt: str = "请将这段音频转换为简短的文字指令，不要解释，只要指令文字"):
        self.model_name = model_name
        self.prompt = prompt
        self.client = None
        
        # 检查API可用性
        if not VOICE_API_AVAILABLE:
            raise RuntimeError("语音识别API不可用，请检查voice2text.py模块")
            
        # 检查API密钥
        if not os.getenv("DASHSCOPE_API_KEY"):
            raise RuntimeError("请设置DASHSCOPE_API_KEY环境变量")
        
        # 初始化客户端
        try:
            self.client = create_voice_client()
            logger.info(f"语音识别器初始化成功，模型: {model_name}")
        except Exception as e:
            logger.error(f"语音识别器初始化失败: {e}")
            raise
    
    def recognize_from_file(self, audio_file_path: str, custom_prompt: Optional[str] = None) -> str:
        """
        函数名称：recognize_from_file
        功能描述：从音频文件识别语音转文字
        参数说明：
            - audio_file_path：音频文件路径
            - custom_prompt：自定义识别提示词，可选
        返回值：str，识别的文字内容
        """
        if not Path(audio_file_path).exists():
            raise FileNotFoundError(f"音频文件不存在: {audio_file_path}")
        
        try:
            # 使用自定义提示词或默认提示词
            prompt = custom_prompt or self.prompt
            
            # 调用语音识别API
            logger.info(f"开始识别音频文件: {audio_file_path}")
            result = audio_to_text_from_file(audio_file_path, prompt)
            
            # 后处理识别结果
            cleaned_result = self._clean_recognition_result(result)
            
            logger.info(f"语音识别完成: {cleaned_result[:50]}...")
            return cleaned_result
            
        except Exception as e:
            error_msg = f"语音识别失败: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
    
    def _clean_recognition_result(self, text: str) -> str:
        """
        函数名称：_clean_recognition_result
        功能描述：清理和优化识别结果
        参数说明：
            - text：原始识别文本
        返回值：str，清理后的文本
        """
        if not text:
            return ""
        
        # 去除前后空白字符
        cleaned = text.strip()
        
        # 去除常见的识别错误标记
        unwanted_phrases = [
            "请将这段音频转换为",
            "音频内容是",
            "音频中说的是",
            "这段音频在说",
            "音频转文字结果：",
        ]
        
        for phrase in unwanted_phrases:
            if cleaned.startswith(phrase):
                cleaned = cleaned[len(phrase):].strip()
        
        # 去除标点符号开头
        while cleaned and cleaned[0] in '：:，,。.':
            cleaned = cleaned[1:].strip()
        
        # 确保不为空
        if not cleaned:
            cleaned = text.strip()  # 如果过度清理，返回原始文本
        
        return cleaned
    
    def is_silent_audio(self, audio_file_path: str) -> bool:
        """
        函数名称：is_silent_audio
        功能描述：检测音频是否为静音（简单检查，避免重复API调用）
        参数说明：
            - audio_file_path：音频文件路径
        返回值：bool，是否为静音
        """
        try:
            # 简单检查：文件大小太小可能是静音
            file_size = os.path.getsize(audio_file_path)
            if file_size < 2000:  # 小于2KB认为可能是静音（调高阈值）
                logger.info(f"文件太小({file_size} bytes)，可能是静音")
                return True
            
            # 不进行API调用，避免重复识别
            # 让后续的语音识别来处理，如果真的是静音会返回空结果
            return False
            
        except Exception as e:
            logger.error(f"静音检测失败: {e}")
            return False  # 出错时不认为是静音，让后续处理
    
    def batch_recognize(self, audio_files: list[str]) -> dict[str, str]:
        """
        函数名称：batch_recognize
        功能描述：批量识别多个音频文件
        参数说明：
            - audio_files：音频文件路径列表
        返回值：dict，文件路径到识别结果的映射
        """
        results = {}
        
        for audio_file in audio_files:
            try:
                result = self.recognize_from_file(audio_file)
                results[audio_file] = result
                logger.info(f"批量识别完成: {Path(audio_file).name}")
            except Exception as e:
                results[audio_file] = f"识别失败: {str(e)}"
                logger.error(f"批量识别失败 {audio_file}: {e}")
        
        return results


class VoiceCommandProcessor:
    """
    函数名称：VoiceCommandProcessor
    功能描述：语音指令处理器，专门处理QT控制相关的语音指令
    参数说明：
        - recognizer：SpeechRecognizer实例
    返回值：VoiceCommandProcessor实例
    """
    
    def __init__(self, recognizer: SpeechRecognizer):
        self.recognizer = recognizer
        
        # QT控制指令的优化提示词  
        self.qt_prompts = {
            'login': "将音频转为简短文字，只要指令内容：如'登录账号xxx密码xxx'",
            'button': "将音频转为简短文字，只要指令内容：如'点击测试按钮'", 
            'status': "将音频转为简短文字，只要指令内容：如'查看状态'",
            'general': "将音频转为简短文字指令，不要解释代码，只要用户说的话"
        }
    
    def process_voice_command(self, audio_file_path: str, command_type: str = 'general') -> str:
        """
        函数名称：process_voice_command
        功能描述：处理语音指令，针对不同类型使用优化提示词
        参数说明：
            - audio_file_path：音频文件路径
            - command_type：指令类型 (login/button/status/general)
        返回值：str，处理后的指令文本
        """
        prompt = self.qt_prompts.get(command_type, self.qt_prompts['general'])
        
        try:
            result = self.recognizer.recognize_from_file(audio_file_path, prompt)
            
            # 根据指令类型进行后处理
            if command_type == 'login':
                return self._process_login_command(result)
            elif command_type == 'button':
                return self._process_button_command(result)
            elif command_type == 'status':
                return self._process_status_command(result)
            else:
                return result
                
        except Exception as e:
            logger.error(f"语音指令处理失败: {e}")
            return f"语音识别失败: {str(e)}"
    
    def _process_login_command(self, text: str) -> str:
        """处理登录指令"""
        # 简单的登录指令标准化
        keywords = ['登录', '账号', '用户名', '密码']
        if any(keyword in text for keyword in keywords):
            return text
        else:
            return f"登录 {text}"
    
    def _process_button_command(self, text: str) -> str:
        """处理按钮指令"""
        if '按钮' not in text and '点击' not in text:
            return f"点击 {text}"
        return text
    
    def _process_status_command(self, text: str) -> str:
        """处理状态查询指令"""
        if '状态' not in text and '查看' not in text:
            return f"查看状态 {text}"
        return text


def test_speech_recognition():
    """测试语音识别功能"""
    print("语音识别测试")
    print("="*40)
    
    try:
        # 创建识别器
        recognizer = SpeechRecognizer()
        processor = VoiceCommandProcessor(recognizer)
        
        print("语音识别器创建成功")
        
        # 检查是否有测试音频文件
        test_audio_dir = Path("temp_audio")
        if test_audio_dir.exists():
            audio_files = list(test_audio_dir.glob("*.wav"))
            if audio_files:
                test_file = audio_files[0]
                print(f"测试文件: {test_file}")
                
                result = recognizer.recognize_from_file(str(test_file))
                print(f"识别结果: {result}")
                
                processed = processor.process_voice_command(str(test_file))
                print(f"处理后: {processed}")
            else:
                print("没有找到测试音频文件")
        else:
            print("临时音频目录不存在")
            
    except Exception as e:
        print(f"测试失败: {e}")


if __name__ == "__main__":
    test_speech_recognition() 