#!/usr/bin/env python3
"""
QT应用语音控制主程序
支持语音输入和文字输入的混合控制模式
"""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path

# 添加当前目录和MCP客户端目录到Python路径
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# 添加MCP客户端路径
mcp_client_dir = current_dir.parent / "Mcp" / "mcp-client"  
sys.path.insert(0, str(mcp_client_dir))

from dotenv import load_dotenv

# 导入MCP客户端模块
from main import MCPClient, LLMClient

# 导入本地语音模块
from voice_chat_session import VoiceChatSession

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_voice_dependencies():
    """
    函数名称：check_voice_dependencies
    功能描述：检查语音功能依赖是否可用
    参数说明：无
    返回值：tuple，(语音录制可用, 语音识别可用, 错误信息)
    """
    audio_available = True
    voice_api_available = True
    errors = []
    
    # 检查音频录制依赖
    try:
        import sounddevice as sd
        import numpy as np
    except ImportError as e:
        audio_available = False
        errors.append(f"音频录制依赖缺失: {e}")
        errors.append("请运行: pip install sounddevice numpy")
    
    # 检查语音API依赖
    try:
        # 检查API密钥
        if not os.getenv("DASHSCOPE_API_KEY"):
            voice_api_available = False
            errors.append("未设置DASHSCOPE_API_KEY环境变量")
        
        # 检查Voice模块
        voice_file = current_dir / "voice2text.py"
        if not voice_file.exists():
            voice_api_available = False
            errors.append(f"语音识别模块不存在: {voice_file}")
            
    except Exception as e:
        voice_api_available = False
        errors.append(f"语音API检查失败: {e}")
    
    return audio_available, voice_api_available, errors


def print_voice_status():
    """
    函数名称：print_voice_status
    功能描述：打印语音功能状态
    参数说明：无
    返回值：bool，语音功能是否完全可用
    """
    print("🎤 语音功能检查")
    print("=" * 30)
    
    audio_ok, voice_api_ok, errors = check_voice_dependencies()
    
    print(f"📢 音频录制: {'✅ 可用' if audio_ok else '❌ 不可用'}")
    print(f"🔊 语音识别: {'✅ 可用' if voice_api_ok else '❌ 不可用'}")
    
    if errors:
        print("\n⚠️  问题列表:")
        for error in errors:
            print(f"   • {error}")
    
    voice_fully_available = audio_ok and voice_api_ok
    
    if voice_fully_available:
        print("\n✅ 语音功能完全可用")
    elif audio_ok and not voice_api_ok:
        print("\n⚠️  可录音但无法识别，将降级到文字模式")
    else:
        print("\n❌ 语音功能不可用，使用文字模式")
    
    print("=" * 30)
    
    return voice_fully_available


def get_voice_config():
    """
    函数名称：get_voice_config
    功能描述：获取语音相关配置
    参数说明：无
    返回值：dict，语音配置字典
    """
    return {
        'voice_enabled': os.getenv('VOICE_ENABLED', 'true').lower() == 'true',
        'voice_model': os.getenv('VOICE_MODEL', 'qwen-omni-turbo-0119'),
        'voice_format': os.getenv('VOICE_FORMAT', 'wav'),
        'sample_rate': int(os.getenv('VOICE_SAMPLE_RATE', '16000')),
        'max_recording_duration': int(os.getenv('MAX_RECORDING_DURATION', '30')),
        'auto_confirm_voice': os.getenv('AUTO_CONFIRM_VOICE', 'false').lower() == 'true',
    }


def load_env_config():
    """
    函数名称：load_env_config
    功能描述：加载环境变量配置（优先使用voice目录的配置文件）
    参数说明：无
    返回值：无
    """
    # 优先加载voice目录的配置文件
    voice_config_file = current_dir / "config.env"
    mcp_config_file = mcp_client_dir / "config.env"
    
    if voice_config_file.exists():
        load_dotenv(voice_config_file)
        logger.info(f"从 {voice_config_file} 加载环境变量")
    elif mcp_config_file.exists():
        load_dotenv(mcp_config_file)
        logger.info(f"从 {mcp_config_file} 加载环境变量")
    else:
        logger.warning("未找到配置文件，使用系统环境变量")


async def main():
    """
    函数名称：main
    功能描述：语音版主函数，初始化并启动语音聊天会话
    参数说明：无
    返回值：无
    """
    print("🎙️ QT应用语音控制助手")
    print("=" * 40)
    
    # 加载环境变量配置
    load_env_config()
    
    # 检查语音功能状态
    voice_fully_available = print_voice_status()
    voice_config = get_voice_config()
    
    # 如果用户禁用了语音功能
    if not voice_config['voice_enabled']:
        print("⚠️  用户已禁用语音功能（VOICE_ENABLED=false）")
        voice_fully_available = False
    
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
        print("❌ 请在config.env文件中设置API密钥")
        print("   支持: DASHSCOPE_API_KEY, OPENAI_API_KEY, ZHIPUAI_API_KEY, DEEPSEEK_API_KEY")
        return
        
    llm_client = LLMClient(
        model_name=model_name,
        api_key=api_key,
        url=base_url
    )
    
    print(f"\n🤖 LLM配置:")
    print(f"   模型: {model_name}")
    print(f"   地址: {base_url}")
    
    # 创建语音聊天会话
    voice_chat_session = VoiceChatSession(
        llm_client=llm_client, 
        mcp_client=mcp_client, 
        voice_enabled=voice_fully_available
    )
    
    try:
        # 连接到MCP服务器
        mcp_server_url = os.getenv('MCP_SERVER_URL', 'http://localhost:8000')
        print(f"\n🔗 MCP服务器: {mcp_server_url}")
        await mcp_client.connect_to_server(mcp_server_url)
        
        # 获取可用工具列表并格式化为系统提示的一部分
        tools = await mcp_client.list_tools()
        tools_description = json.dumps(tools, ensure_ascii=False, indent=2)

        # QT应用控制专用系统提示词（语音优化版）
        system_message = f'''
        你是一个QT应用程序语音控制助手，专门帮助用户通过语音或文字操作QT应用程序。

        可用工具：{tools_description}

        语音交互优化规则：
        1、语音识别结果可能包含口语化表达，需要智能理解用户意图
        2、支持模糊匹配，如"登陆"→"登录"，"用户名wyx密码124"→提取用户名和密码
        3、对于不完整的语音指令，主动询问缺失信息

        响应规则：
        1、当识别到操作指令时，返回严格的JSON格式：
        {{
            "tool": "tool-name",
            "arguments": {{
                "argument-name": "value"
            }}
        }}

        2、禁止包含以下内容：
         - Markdown标记（如```json）
         - 自然语言解释前缀
         - 多余的格式化符号

        3、常见语音指令映射：
         - "登录" "登陆" "账号登录" → 使用 login 工具
         - "点击测试" "测试按钮" "按钮测试" → 使用 test_button 工具  
         - "查看状态" "应用状态" "当前状态" → 使用 get_state 工具

        4、语音识别容错：
         - "登录账号wyx密码124" → {{"tool":"login","arguments":{{"account":"wyx","password":"124"}}}}
         - "账号是wyx，密码是124，登录" → {{"tool":"login","arguments":{{"account":"wyx","password":"124"}}}}
         - "测试一下按钮" → {{"tool":"test_button","arguments":{{"random_string":"test"}}}}

        5、执行结果反馈：
         - 将工具执行结果转化为友好的中文回应
         - 突出操作成功/失败状态
         - 提供必要的后续建议

        语音识别优化提示：
        - 理解口语化表达和方言
        - 智能提取关键信息（用户名、密码等）
        - 支持自然语言到结构化指令的转换
        '''
        
        # 启动语音聊天会话
        await voice_chat_session.start(system_message)

    except Exception as e:
        logger.error(f"语音主程序错误: {e}")
        print(f"启动失败: {e}")
        
        # 提供详细的错误诊断
        if "MCP" in str(e):
            print("\n💡 MCP连接问题解决方案:")
            print("   1. 确保MCP服务器正在运行: cd ../mcp-server-qt && python main.py")
            print("   2. 检查端口配置: MCP_SERVER_URL=http://localhost:8000")
        elif "API" in str(e) or "key" in str(e).lower():
            print("\n💡 API密钥问题解决方案:")
            print("   1. 检查config.env中的API密钥设置")
            print("   2. 确保网络连接正常")
        elif "语音" in str(e) or "voice" in str(e).lower():
            print("\n💡 语音功能问题解决方案:")
            print("   1. 安装音频依赖: pip install sounddevice numpy")
            print("   2. 检查voice2text.py模块")
            print("   3. 可以使用文字模式: cd ../Mcp/mcp-client && python main.py")
            
    finally:
        # 确保资源被清理
        await voice_chat_session.cleanup()


def interactive_mode_selection():
    """
    函数名称：interactive_mode_selection
    功能描述：交互式选择运行模式
    参数说明：无
    返回值：str，选择的模式 (voice/text/auto)
    """
    print("\n🎯 运行模式选择:")
    print("1. 语音+文字混合模式 (推荐)")
    print("2. 纯文字模式")
    print("3. 自动检测")
    
    choice = input("请选择模式 (1-3, 默认1): ").strip()
    
    if choice == "2":
        return "text"
    elif choice == "3":
        return "auto"
    else:
        return "voice"


if __name__ == "__main__":
    try:
        # 检查命令行参数
        if len(sys.argv) > 1:
            if sys.argv[1] == "--voice-only":
                # 强制语音模式
                os.environ['VOICE_ENABLED'] = 'true'
                print("🎤 强制启用语音模式")
            elif sys.argv[1] == "--text-only":
                # 强制文字模式
                os.environ['VOICE_ENABLED'] = 'false'
                print("📝 强制启用文字模式")
            elif sys.argv[1] == "--interactive":
                # 交互式选择模式
                mode = interactive_mode_selection()
                if mode == "text":
                    os.environ['VOICE_ENABLED'] = 'false'
                elif mode == "voice":
                    os.environ['VOICE_ENABLED'] = 'true'
                # auto模式保持默认配置
        
        # 运行主程序
        asyncio.run(main())
        
    except KeyboardInterrupt:
        print("\n🛑 用户中断，程序退出")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 程序异常退出: {e}")
        sys.exit(1) 