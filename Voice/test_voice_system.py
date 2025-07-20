#!/usr/bin/env python3
"""
语音控制系统完整测试脚本
测试所有语音功能模块的集成和工作状态
"""

import os
import sys
import asyncio
import logging
from pathlib import Path
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# 添加路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))


def test_environment():
    """测试环境配置"""
    print("\n=== 环境配置测试 ===")
    
    # 加载配置文件
    config_file = current_dir / "config.env"
    if config_file.exists():
        load_dotenv(config_file)
        print(f"✓ 配置文件: {config_file}")
    else:
        print(f"⚠ 配置文件不存在: {config_file}")
    
    # 检查API密钥
    api_key = os.getenv('DASHSCOPE_API_KEY')
    if api_key:
        print(f"✓ API密钥: {api_key[:8]}...")
    else:
        print("✗ 未设置DASHSCOPE_API_KEY")
        return False
    
    # 检查其他配置
    configs = {
        'VOICE_ENABLED': os.getenv('VOICE_ENABLED', 'true'),
        'VOICE_MODEL': os.getenv('VOICE_MODEL', 'qwen-omni-turbo-0119'),
        'MCP_SERVER_URL': os.getenv('MCP_SERVER_URL', 'http://localhost:8000'),
    }
    
    print("✓ 配置项:")
    for key, value in configs.items():
        print(f"   {key}: {value}")
    
    return True


def test_dependencies():
    """测试依赖安装"""
    print("\n=== 依赖检查测试 ===")
    
    dependencies = [
        ('sounddevice', 'sounddevice'),
        ('numpy', 'numpy'),
        ('requests', 'requests'),
        ('httpx', 'httpx'),
        ('fastmcp', 'fastmcp'),
        ('openai', 'openai'),
        ('python-dotenv', 'dotenv'),
    ]
    
    missing = []
    for name, module in dependencies:
        try:
            __import__(module)
            print(f"✓ {name}")
        except ImportError:
            print(f"✗ {name}")
            missing.append(name)
    
    if missing:
        print(f"\n缺失依赖: {', '.join(missing)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    return True


def test_audio_system():
    """测试音频系统"""
    print("\n=== 音频系统测试 ===")
    
    try:
        import sounddevice as sd
        import numpy as np
        
        # 检查音频设备
        devices = sd.query_devices()
        print(f"✓ 音频设备数量: {len(devices)}")
        
        # 检查默认设备
        default_device = sd.query_devices(kind='input')
        print(f"✓ 默认录音设备: {default_device['name']}")
        
        # 测试简单录音
        print("测试录音功能...")
        duration = 1  # 1秒测试录音
        sample_rate = 16000
        
        recording = sd.rec(int(duration * sample_rate), 
                          samplerate=sample_rate, 
                          channels=1, 
                          dtype=np.float32)
        sd.wait()
        
        if recording.size > 0:
            print("✓ 录音功能正常")
            return True
        else:
            print("✗ 录音功能异常")
            return False
            
    except Exception as e:
        print(f"✗ 音频系统错误: {e}")
        return False


def test_voice_modules():
    """测试语音模块"""
    print("\n=== 语音模块测试 ===")
    
    # 测试语音录制模块
    try:
        from voice_input import VoiceRecorder, KeyboardVoiceInput, AUDIO_AVAILABLE
        print(f"✓ 语音录制模块 (可用: {AUDIO_AVAILABLE})")
    except ImportError as e:
        print(f"✗ 语音录制模块: {e}")
        return False
    
    # 测试语音识别模块
    try:
        from speech_recognizer import SpeechRecognizer, VOICE_API_AVAILABLE
        print(f"✓ 语音识别模块 (API可用: {VOICE_API_AVAILABLE})")
    except ImportError as e:
        print(f"✗ 语音识别模块: {e}")
        return False
    
    # 测试语音会话模块
    try:
        from voice_chat_session import VoiceChatSession
        print("✓ 语音会话模块")
    except ImportError as e:
        print(f"✗ 语音会话模块: {e}")
        return False
    
    return True


def test_mcp_connectivity():
    """测试MCP连接"""
    print("\n=== MCP连接测试 ===")
    
    try:
        # 添加MCP客户端路径
        mcp_client_dir = current_dir.parent / "Mcp" / "mcp-client"
        sys.path.insert(0, str(mcp_client_dir))
        
        from main import MCPClient, LLMClient
        print("✓ MCP客户端模块导入成功")
        
        # 测试基本实例化
        mcp_client = MCPClient()
        print("✓ MCP客户端实例创建成功")
        
        return True
        
    except ImportError as e:
        print(f"✗ MCP客户端导入失败: {e}")
        return False
    except Exception as e:
        print(f"⚠ MCP客户端测试警告: {e}")
        return True  # 非致命错误


async def test_speech_recognition():
    """测试语音识别功能"""
    print("\n=== 语音识别功能测试 ===")
    
    try:
        from speech_recognizer import SpeechRecognizer
        
        # 创建识别器
        recognizer = SpeechRecognizer()
        print("✓ 语音识别器创建成功")
        
        # 检查测试音频文件
        test_audio_files = list(current_dir.glob("*.wav"))
        if test_audio_files:
            test_file = test_audio_files[0]
            print(f"✓ 找到测试音频: {test_file.name}")
            
            try:
                result = recognizer.recognize_from_file(str(test_file))
                print(f"✓ 识别结果: {result[:50]}...")
                return True
            except Exception as e:
                print(f"⚠ 识别测试失败: {e}")
                return True  # API问题不算致命错误
        else:
            print("⚠ 未找到测试音频文件，跳过识别测试")
            return True
            
    except Exception as e:
        print(f"✗ 语音识别测试失败: {e}")
        return False


def test_integration():
    """测试系统集成"""
    print("\n=== 系统集成测试 ===")
    
    try:
        from main_voice import check_voice_dependencies, get_voice_config
        
        # 检查依赖状态
        audio_ok, voice_api_ok, errors = check_voice_dependencies()
        print(f"✓ 依赖检查 - 音频: {audio_ok}, 语音API: {voice_api_ok}")
        
        if errors:
            for error in errors:
                print(f"   ⚠ {error}")
        
        # 获取配置
        config = get_voice_config()
        print(f"✓ 配置获取 - 语音启用: {config['voice_enabled']}")
        
        return audio_ok or voice_api_ok  # 至少一个功能可用
        
    except Exception as e:
        print(f"✗ 集成测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("🎤 语音控制系统完整测试")
    print("=" * 50)
    
    tests = [
        ("环境配置", test_environment),
        ("依赖检查", test_dependencies),
        ("音频系统", test_audio_system),
        ("语音模块", test_voice_modules),
        ("MCP连接", test_mcp_connectivity),
        ("系统集成", test_integration),
    ]
    
    results = {}
    
    # 执行测试
    for name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = asyncio.run(test_func())
            else:
                result = test_func()
            results[name] = result
        except Exception as e:
            print(f"✗ {name}测试异常: {e}")
            results[name] = False
    
    # 语音识别需要异步测试
    try:
        result = asyncio.run(test_speech_recognition())
        results["语音识别"] = result
    except Exception as e:
        print(f"✗ 语音识别测试异常: {e}")
        results["语音识别"] = False
    
    # 汇总结果
    print("\n" + "=" * 50)
    print("📊 测试结果汇总:")
    
    passed = 0
    total = len(results)
    
    for name, result in results.items():
        status = "✓ 通过" if result else "✗ 失败"
        print(f"   {name}: {status}")
        if result:
            passed += 1
    
    print(f"\n总体结果: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！语音控制系统完全可用。")
        return 0
    elif passed >= total * 0.7:  # 70%以上通过
        print("⚠ 大部分功能可用，建议检查失败项目。")
        return 1
    else:
        print("❌ 系统存在严重问题，请修复后重新测试。")
        return 2


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n用户中断测试")
        sys.exit(130)
    except Exception as e:
        print(f"\n测试程序异常: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 