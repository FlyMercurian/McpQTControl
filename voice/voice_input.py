"""
语音输入模块
支持按键录音、实时状态显示和音频文件保存
"""

import os
import sys
import wave
import time
import threading
from pathlib import Path
from typing import Optional, Callable
import logging

try:
    import sounddevice as sd
    import numpy as np
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False
    logging.warning("sounddevice未安装，语音功能不可用。请运行: pip install sounddevice numpy")

logger = logging.getLogger(__name__)


class VoiceRecorder:
    """
    函数名称：VoiceRecorder
    功能描述：语音录制类，支持按键录音和实时状态显示
    参数说明：
        - sample_rate：采样率，默认16000
        - channels：声道数，默认1（单声道）
        - max_duration：最大录音时长（秒），默认30
    返回值：VoiceRecorder实例
    """
    
    def __init__(self, sample_rate: int = 16000, channels: int = 1, max_duration: int = 30):
        self.sample_rate = sample_rate
        self.channels = channels
        self.max_duration = max_duration
        self.audio_data = []
        self.is_recording = False
        self.record_thread = None
        self.start_time = 0
        
        # 检查音频设备可用性
        if not AUDIO_AVAILABLE:
            raise RuntimeError("sounddevice未安装，无法使用语音功能")
            
        # 创建临时目录存放录音文件 - 在voice目录下
        temp_dir_name = os.getenv('TEMP_AUDIO_DIR', 'temp_audio')
        self.temp_dir = Path(__file__).parent / temp_dir_name
        self.temp_dir.mkdir(exist_ok=True)
    
    def _audio_callback(self, indata, frames, time, status):
        """
        函数名称：_audio_callback
        功能描述：音频录制回调函数
        参数说明：
            - indata：输入音频数据
            - frames：音频帧数
            - time：时间信息
            - status：状态信息
        返回值：无
        """
        if status:
            logger.warning(f"Audio status: {status}")
        
        if self.is_recording:
            self.audio_data.append(indata.copy())
    
    def start_recording(self) -> bool:
        """
        函数名称：start_recording
        功能描述：开始录音
        参数说明：无
        返回值：bool，是否成功开始录音
        """
        try:
            if self.is_recording:
                return False
                
            self.audio_data = []
            self.is_recording = True
            self.start_time = time.time()
            
            # 启动录音流
            self.stream = sd.InputStream(
                channels=self.channels,
                samplerate=self.sample_rate,
                callback=self._audio_callback,
                dtype=np.float32
            )
            self.stream.start()
            
            logger.info("开始录音...")
            return True
            
        except Exception as e:
            logger.error(f"启动录音失败: {e}")
            self.is_recording = False
            return False
    
    def stop_recording(self) -> float:
        """
        函数名称：stop_recording
        功能描述：停止录音
        参数说明：无
        返回值：float，录音时长（秒）
        """
        if not self.is_recording:
            return 0.0
            
        self.is_recording = False
        duration = time.time() - self.start_time
        
        try:
            self.stream.stop()
            self.stream.close()
            logger.info(f"录音结束，时长: {duration:.2f}秒")
        except Exception as e:
            logger.error(f"停止录音失败: {e}")
        
        return duration
    
    def save_recording(self, filename: Optional[str] = None) -> str:
        """
        函数名称：save_recording
        功能描述：保存录音到文件
        参数说明：
            - filename：文件名，默认自动生成
        返回值：str，保存的文件路径
        """
        if not self.audio_data:
            raise ValueError("没有录音数据可保存")
        
        if filename is None:
            timestamp = int(time.time())
            filename = f"voice_record_{timestamp}.wav"
        
        filepath = self.temp_dir / filename
        
        # 合并音频数据
        audio_array = np.concatenate(self.audio_data, axis=0)
        
        # 转换为16位整数格式
        audio_int16 = (audio_array * 32767).astype(np.int16)
        
        # 保存为WAV文件
        with wave.open(str(filepath), 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)  # 16位 = 2字节
            wf.setframerate(self.sample_rate)
            wf.writeframes(audio_int16.tobytes())
        
        logger.info(f"录音已保存: {filepath}")
        return str(filepath)
    
    def get_recording_duration(self) -> float:
        """
        函数名称：get_recording_duration
        功能描述：获取当前录音时长
        参数说明：无
        返回值：float，录音时长（秒）
        """
        if not self.is_recording:
            return 0.0
        return time.time() - self.start_time
    
    def cleanup(self):
        """
        函数名称：cleanup
        功能描述：清理临时文件
        参数说明：无
        返回值：无
        """
        try:
            if hasattr(self, 'stream') and self.stream:
                if self.is_recording:
                    self.stop_recording()
                    
            # 删除临时音频文件
            if self.temp_dir.exists():
                for file in self.temp_dir.glob("*.wav"):
                    try:
                        file.unlink()
                    except:
                        pass
                        
        except Exception as e:
            logger.error(f"清理资源失败: {e}")


class KeyboardVoiceInput:
    """
    函数名称：KeyboardVoiceInput
    功能描述：键盘控制语音输入类，支持按键录音
    参数说明：
        - recorder：VoiceRecorder实例
        - trigger_key：触发录音的按键，默认'v'
    返回值：KeyboardVoiceInput实例
    """
    
    def __init__(self, recorder: VoiceRecorder, trigger_key: str = 'v'):
        self.recorder = recorder
        self.trigger_key = trigger_key.lower()
        self.is_monitoring = False
        self.monitor_thread = None
        
        # 检查平台支持
        try:
            if sys.platform == 'win32':
                import msvcrt
                self.input_method = 'msvcrt'
            else:
                import tty, termios
                self.input_method = 'termios'
        except ImportError:
            logger.warning("键盘监听功能不可用")
            self.input_method = None
    
    def wait_for_voice_input(self, prompt: str = "按 [V键] 开始录音，再按 [V键] 结束") -> Optional[str]:
        """
        函数名称：wait_for_voice_input
        功能描述：等待语音输入，支持按键控制录音
        参数说明：
            - prompt：提示信息
        返回值：Optional[str]，录音文件路径，如果取消则返回None
        """
        if not AUDIO_AVAILABLE:
            print("语音功能不可用，请安装 sounddevice 和 numpy")
            return None
            
        print(f"🎤 {prompt}")
        print("操作方式：按V键开始→录音中→再按V键结束；ESC取消；回车跳过")
        
        if sys.platform == 'win32':
            return self._windows_voice_input()
        else:
            return self._unix_voice_input()
    
    def _windows_voice_input(self) -> Optional[str]:
        """Windows平台的语音输入处理 - 修复版：按一次开始，再按一次结束"""
        import msvcrt
        
        recording_state = False  # 录音状态
        
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                
                # 处理特殊键
                if key == b'\x1b':  # ESC
                    if recording_state:
                        # 如果正在录音，停止录音
                        self.recorder.stop_recording()
                        print("\n录音已取消")
                        recording_state = False
                        continue
                    else:
                        print("\n语音输入已取消")
                        return None
                        
                elif key == b'\r':  # Enter
                    if recording_state:
                        # 如果正在录音，结束录音
                        duration = self.recorder.stop_recording()
                        if duration > 0.5:
                            filepath = self.recorder.save_recording()
                            print(f"\n录音完成 ({duration:.2f}秒)")
                            return filepath
                        else:
                            print("\n录音时间太短，已忽略")
                            recording_state = False
                            continue
                    else:
                        print("\n跳过语音输入")
                        return None
                        
                elif key.lower() == self.trigger_key.encode():
                    if not recording_state:
                        # V键按下，开始录音
                        if self.recorder.start_recording():
                            print("\n🎤 开始录音... (再按V键或回车结束，ESC取消)")
                            recording_state = True
                        else:
                            print("\n录音启动失败")
                    else:
                        # V键再次按下，结束录音
                        duration = self.recorder.stop_recording()
                        if duration > 0.5:
                            filepath = self.recorder.save_recording()
                            print(f"\n录音完成 ({duration:.2f}秒)")
                            return filepath
                        else:
                            print("\n录音时间太短，已忽略")
                            recording_state = False
                            continue
            
            # 如果正在录音，检查时长和显示进度
            if recording_state:
                current_duration = self.recorder.get_recording_duration()
                
                # 检查最大录音时长
                if current_duration >= self.recorder.max_duration:
                    duration = self.recorder.stop_recording()
                    filepath = self.recorder.save_recording()
                    print(f"\n达到最大录音时长 ({duration:.2f}秒)")
                    return filepath
                
                # 显示录音进度
                progress = "█" * min(int(current_duration), 50)  # 限制进度条长度
                print(f"\r🎤 正在录音... {progress} ({current_duration:.1f}s) [V键结束]", end="", flush=True)
                time.sleep(0.1)
            else:
                time.sleep(0.01)
    
    def _unix_voice_input(self) -> Optional[str]:
        """Unix/Linux/Mac平台的语音输入处理"""
        print("Unix平台暂不支持按键录音，请使用文字输入模式")
        return None


def test_voice_input():
    """测试语音输入功能"""
    print("语音输入测试")
    print("="*40)
    
    try:
        recorder = VoiceRecorder()
        voice_input = KeyboardVoiceInput(recorder)
        
        result = voice_input.wait_for_voice_input()
        
        if result:
            print(f"录音文件: {result}")
            print(f"文件大小: {os.path.getsize(result)} bytes")
        else:
            print("未录制音频")
            
        recorder.cleanup()
        
    except Exception as e:
        print(f"测试失败: {e}")


if __name__ == "__main__":
    test_voice_input() 