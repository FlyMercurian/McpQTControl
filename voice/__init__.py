"""
语音控制模块包
包含语音录制、识别、会话管理和主程序等功能
"""

__version__ = "1.0.0"
__author__ = "McpQTControl"

# 导出主要类和函数
from .voice_input import VoiceRecorder, KeyboardVoiceInput
from .speech_recognizer import SpeechRecognizer
from .voice_chat_session import VoiceChatSession

__all__ = [
    'VoiceRecorder',
    'KeyboardVoiceInput', 
    'SpeechRecognizer',
    'VoiceChatSession'
] 