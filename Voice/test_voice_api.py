#!/usr/bin/env python3
"""
测试阿里云语音识别API
验证voice2text.py模块是否正常工作
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 添加当前目录到路径
sys.path.insert(0, str(Path(__file__).parent))

def test_api_with_url():
    """测试URL方式的语音识别"""
    print("🌐 测试URL方式语音识别...")
    
    try:
        from voice2text import audio_to_text_from_url
        
        # 使用阿里云提供的测试音频
        test_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav"
        
        result = audio_to_text_from_url(test_url, "这段音频在说什么")
        print(f"✅ URL识别成功: {result}")
        return True
        
    except Exception as e:
        print(f"❌ URL识别失败: {e}")
        return False

def test_api_with_file():
    """测试本地文件方式的语音识别"""
    print("\n📁 测试本地文件语音识别...")
    
    # 寻找最近录制的音频文件
    audio_dir = Path("../mcp-client/temp_audio")
    if audio_dir.exists():
        audio_files = list(audio_dir.glob("*.wav"))
        if audio_files:
            # 选择最新的文件
            latest_file = max(audio_files, key=lambda x: x.stat().st_mtime)
            print(f"📂 测试文件: {latest_file}")
            
            try:
                from voice2text import audio_to_text_from_file
                
                result = audio_to_text_from_file(str(latest_file), "请转换为文字")
                print(f"✅ 文件识别成功: {result}")
                return True
                
            except Exception as e:
                print(f"❌ 文件识别失败: {e}")
                print(f"   文件大小: {latest_file.stat().st_size} bytes")
                return False
        else:
            print("⚠️ 没有找到音频文件")
            return False
    else:
        print("⚠️ 音频目录不存在")
        return False

def main():
    """主测试函数"""
    print("🧪 阿里云语音识别API测试")
    print("=" * 40)
    
    # 加载环境变量
    env_file = Path("../mcp-client/config.env")
    if env_file.exists():
        load_dotenv(env_file)
        print("✅ 加载配置文件")
    else:
        print("⚠️ 配置文件不存在，使用系统环境变量")
    
    # 检查API密钥
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        print("❌ 未设置DASHSCOPE_API_KEY")
        return False
    
    print(f"✅ API密钥: {api_key[:8]}...")
    
    # 测试URL方式
    url_success = test_api_with_url()
    
    # 测试文件方式
    file_success = test_api_with_file()
    
    print("\n📊 测试结果:")
    print(f"  URL方式: {'✅ 成功' if url_success else '❌ 失败'}")
    print(f"  文件方式: {'✅ 成功' if file_success else '❌ 失败'}")
    
    if url_success and not file_success:
        print("\n💡 URL方式正常，文件方式有问题")
        print("   可能是Base64编码或文件格式问题")
    elif not url_success:
        print("\n💡 API配置或网络问题")
        print("   请检查API密钥和网络连接")
    
    return url_success or file_success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ 测试异常: {e}")
        sys.exit(1) 