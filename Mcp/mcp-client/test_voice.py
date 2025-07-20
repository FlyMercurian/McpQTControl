#!/usr/bin/env python3
"""
语音功能测试脚本
测试语音录制和识别功能是否正常工作
"""

import asyncio
import os
import sys
from pathlib import Path

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

def test_dependencies():
    """测试依赖包是否安装"""
    print("🔍 检查依赖包...")
    
    dependencies = {
        'sounddevice': '音频录制',
        'numpy': '数据处理',
        'openai': 'API客户端',
        'fastmcp': 'MCP框架',
        'dotenv': '环境变量'
    }
    
    missing = []
    for pkg, desc in dependencies.items():
        try:
            __import__(pkg)
            print(f"  ✅ {pkg} ({desc})")
        except ImportError:
            print(f"  ❌ {pkg} ({desc}) - 未安装")
            missing.append(pkg)
    
    if missing:
        print(f"\n⚠️  缺少依赖: {', '.join(missing)}")
        print("请运行: pip install -r requirements.txt")
        return False
    else:
        print("✅ 所有依赖已安装")
        return True

def test_environment():
    """测试环境配置"""
    print("\n🔍 检查环境配置...")
    
    # 加载配置文件
    config_file = Path(__file__).parent / "config.env"
    if config_file.exists():
        load_dotenv(config_file)
        print(f"  ✅ 配置文件: {config_file.name}")
    else:
        print(f"  ⚠️  配置文件不存在: {config_file.name}")
    
    # 检查API密钥
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if api_key:
        masked_key = api_key[:8] + "..." if len(api_key) > 8 else "***"
        print(f"  ✅ API密钥: {masked_key}")
    else:
        print("  ❌ 未设置 DASHSCOPE_API_KEY")
        return False
    
    # 检查语音配置
    voice_enabled = os.getenv('VOICE_ENABLED', 'true').lower() == 'true'
    voice_model = os.getenv('VOICE_MODEL', 'qwen-omni-turbo-0119')
    sample_rate = os.getenv('VOICE_SAMPLE_RATE', '16000')
    
    print(f"  ✅ 语音功能: {'启用' if voice_enabled else '禁用'}")
    print(f"  ✅ 语音模型: {voice_model}")
    print(f"  ✅ 采样率: {sample_rate}Hz")
    
    return True

def test_voice_recording():
    """测试语音录制功能"""
    print("\n🎤 测试语音录制...")
    
    try:
        from voice_input import VoiceRecorder, KeyboardVoiceInput, AUDIO_AVAILABLE
        
        if not AUDIO_AVAILABLE:
            print("  ❌ 音频录制功能不可用")
            return False
        
        print("  ✅ 音频模块导入成功")
        
        # 创建录音器
        recorder = VoiceRecorder(sample_rate=16000, max_duration=5)
        print("  ✅ 录音器创建成功")
        
        # 创建键盘输入
        voice_input = KeyboardVoiceInput(recorder)
        print("  ✅ 键盘输入监听器创建成功")
        
        # 清理资源
        recorder.cleanup()
        print("  ✅ 资源清理完成")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 语音录制测试失败: {e}")
        return False

def test_speech_recognition():
    """测试语音识别功能"""
    print("\n🔊 测试语音识别...")
    
    try:
        from speech_recognizer import SpeechRecognizer, VOICE_API_AVAILABLE
        
        if not VOICE_API_AVAILABLE:
            print("  ❌ 语音识别API不可用")
            return False
        
        print("  ✅ 语音识别模块导入成功")
        
        # 创建识别器
        recognizer = SpeechRecognizer()
        print("  ✅ 语音识别器创建成功")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 语音识别测试失败: {e}")
        return False

def test_integration():
    """测试集成功能"""
    print("\n🔗 测试功能集成...")
    
    try:
        from voice_chat_session import VoiceChatSession
        print("  ✅ 语音聊天会话模块导入成功")
        
        # 模拟客户端测试
        class MockLLMClient:
            def get_response(self, messages):
                return "测试响应"
        
        class MockMCPClient:
            async def cleanup(self):
                pass
        
        llm_client = MockLLMClient()
        mcp_client = MockMCPClient()
        
        # 创建语音会话（测试模式）
        voice_session = VoiceChatSession(
            llm_client=llm_client,
            mcp_client=mcp_client,
            voice_enabled=True
        )
        
        print(f"  ✅ 语音会话创建成功")
        print(f"  ✅ 语音功能状态: {'启用' if voice_session.voice_enabled else '禁用'}")
        
        # 清理资源
        asyncio.run(voice_session.cleanup())
        print("  ✅ 集成测试完成")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 集成测试失败: {e}")
        return False

def test_voice_path():
    """测试Voice目录路径"""
    print("\n📁 测试Voice目录...")
    
    voice_dir = Path(__file__).parent.parent.parent / "Voice"
    voice_file = voice_dir / "voice2text.py"
    
    print(f"  Voice目录: {voice_dir}")
    print(f"  voice2text.py: {voice_file}")
    
    if voice_dir.exists():
        print("  ✅ Voice目录存在")
    else:
        print("  ❌ Voice目录不存在")
        return False
    
    if voice_file.exists():
        print("  ✅ voice2text.py文件存在")
    else:
        print("  ❌ voice2text.py文件不存在")
        return False
    
    return True

def main():
    """主测试函数"""
    print("🧪 QT语音控制功能测试")
    print("=" * 50)
    
    tests = [
        ("依赖检查", test_dependencies),
        ("环境配置", test_environment),
        ("Voice目录", test_voice_path),
        ("语音录制", test_voice_recording),
        ("语音识别", test_speech_recognition),
        ("功能集成", test_integration)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"  ❌ {test_name}测试异常: {e}")
            results[test_name] = False
    
    # 测试总结
    print("\n📊 测试总结")
    print("=" * 30)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✅ 通过" if passed_test else "❌ 失败"
        print(f"  {test_name}: {status}")
    
    print(f"\n🎯 总体结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！语音功能准备就绪")
        print("\n🚀 可以运行:")
        print("   python main_voice.py")
    elif passed >= total * 0.8:
        print("⚠️  部分功能可用，建议检查失败项")
        print("\n🚀 可尝试运行:")
        print("   python main_voice.py --text-only")
    else:
        print("❌ 多项测试失败，请解决问题后重试")
        print("\n🔧 建议:")
        print("   1. 安装缺失依赖: pip install -r requirements.txt")
        print("   2. 检查config.env配置")
        print("   3. 确认Voice/voice2text.py存在")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 测试被用户中断")
        sys.exit(0) 