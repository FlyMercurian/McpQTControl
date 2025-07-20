#!/usr/bin/env python3
"""
QT应用控制 MCP 客户端启动脚本
提供环境检查、配置向导和快速启动功能
"""

import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv


def check_dependencies():
    """
    函数名称：check_dependencies
    功能描述：检查必要的依赖是否已安装
    参数说明：无
    返回值：bool，是否所有依赖都已安装
    """
    required_packages = [
        'httpx', 'openai', 'fastmcp'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少以下依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    
    print("✅ 所有依赖包已安装")
    return True


def load_config():
    """
    函数名称：load_config
    功能描述：加载配置文件
    参数说明：无
    返回值：bool，是否成功加载配置
    """
    current_dir = Path(__file__).parent
    config_file = current_dir / "config.env"
    
    if config_file.exists():
        load_dotenv(config_file)
        print(f"✅ 从 {config_file.name} 加载配置")
        return True
    else:
        print(f"⚠️  配置文件 {config_file.name} 不存在，使用系统环境变量")
        return False


def check_environment():
    """
    函数名称：check_environment
    功能描述：检查环境变量配置
    参数说明：无
    返回值：bool，环境是否配置正确
    """
    print("\n=== 环境配置检查 ===")
    
    # 检查API密钥（支持多个提供商）
    api_key = (os.getenv('DASHSCOPE_API_KEY') or 
               os.getenv('OPENAI_API_KEY') or
               os.getenv('ZHIPUAI_API_KEY') or 
               os.getenv('DEEPSEEK_API_KEY'))
    
    model_name = os.getenv('LLM_MODEL_NAME', 'qwen-plus-latest')
    base_url = os.getenv('LLM_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
    server_url = os.getenv('MCP_SERVER_URL', 'http://localhost:8000')
    
    if not api_key:
        print("❌ 未设置API密钥")
        print("请在config.env中设置以下之一:")
        print("  - DASHSCOPE_API_KEY (阿里云通义千问)")
        print("  - OPENAI_API_KEY (OpenAI)")
        print("  - ZHIPUAI_API_KEY (智谱AI)")
        print("  - DEEPSEEK_API_KEY (Deepseek)")
        return False
    else:
        # 识别使用的API提供商
        if os.getenv('DASHSCOPE_API_KEY'):
            provider = "阿里云通义千问"
        elif os.getenv('OPENAI_API_KEY'):
            provider = "OpenAI"
        elif os.getenv('ZHIPUAI_API_KEY'):
            provider = "智谱AI"
        elif os.getenv('DEEPSEEK_API_KEY'):
            provider = "Deepseek"
        else:
            provider = "未知"
            
        masked_key = api_key[:8] + "..." if len(api_key) > 8 else "***"
        print(f"✅ API密钥 ({provider}): {masked_key}")
    
    print(f"✅ 模型名称: {model_name}")
    print(f"✅ API地址: {base_url}")
    print(f"✅ MCP服务器: {server_url}")
    return True


def setup_environment():
    """
    函数名称：setup_environment
    功能描述：引导用户设置环境变量
    参数说明：无
    返回值：bool，设置是否成功
    """
    print("\n=== 环境配置向导 ===")
    
    # 选择LLM提供商
    print("请选择大语言模型提供商:")
    print("1. 阿里云通义千问 (推荐)")
    print("2. OpenAI")
    print("3. 智谱AI")  
    print("4. Deepseek")
    
    choice = input("请输入选择 (1-4, 默认1): ").strip()
    if not choice:
        choice = "1"
    
    # 根据选择设置相应的配置
    if choice == "1":
        api_key = input("请输入 DASHSCOPE_API_KEY: ").strip()
        if not api_key:
            print("❌ API Key 不能为空")
            return False
        os.environ['DASHSCOPE_API_KEY'] = api_key
        os.environ['LLM_MODEL_NAME'] = 'qwen-plus-latest'
        os.environ['LLM_BASE_URL'] = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
        print("✅ 阿里云通义千问配置已设置")
        
    elif choice == "2":
        api_key = input("请输入 OPENAI_API_KEY: ").strip()
        if not api_key:
            print("❌ API Key 不能为空")
            return False
        os.environ['OPENAI_API_KEY'] = api_key
        model = input("请输入模型名称 (默认: gpt-3.5-turbo): ").strip()
        os.environ['LLM_MODEL_NAME'] = model or 'gpt-3.5-turbo'
        os.environ['LLM_BASE_URL'] = 'https://api.openai.com/v1'
        print("✅ OpenAI配置已设置")
        
    elif choice == "3":
        api_key = input("请输入 ZHIPUAI_API_KEY: ").strip()
        if not api_key:
            print("❌ API Key 不能为空")
            return False
        os.environ['ZHIPUAI_API_KEY'] = api_key
        os.environ['LLM_MODEL_NAME'] = 'glm-4'
        os.environ['LLM_BASE_URL'] = 'https://open.bigmodel.cn/api/paas/v4'
        print("✅ 智谱AI配置已设置")
        
    elif choice == "4":
        api_key = input("请输入 DEEPSEEK_API_KEY: ").strip()
        if not api_key:
            print("❌ API Key 不能为空")
            return False
        os.environ['DEEPSEEK_API_KEY'] = api_key
        os.environ['LLM_MODEL_NAME'] = 'deepseek-chat'
        os.environ['LLM_BASE_URL'] = 'https://api.deepseek.com/v1'
        print("✅ Deepseek配置已设置")
        
    else:
        print("❌ 无效的选择")
        return False
    
    # 设置 MCP 服务器地址
    server_url = input("请输入 MCP 服务器地址 (默认: http://localhost:8000): ").strip()
    if not server_url:
        server_url = "http://localhost:8000"
    
    os.environ['MCP_SERVER_URL'] = server_url
    print(f"✅ MCP 服务器地址已设置: {server_url}")
    
    # 询问是否保存到配置文件
    save_config = input("是否保存配置到 config.env 文件? (y/n, 默认n): ").lower().strip()
    if save_config == 'y':
        try:
            config_content = f"""# QT应用控制 MCP 客户端配置文件 (自动生成)

# 大语言模型配置
LLM_MODEL_NAME={os.environ.get('LLM_MODEL_NAME', '')}
LLM_BASE_URL={os.environ.get('LLM_BASE_URL', '')}

# API密钥 (根据选择的提供商)
"""
            if os.getenv('DASHSCOPE_API_KEY'):
                config_content += f"DASHSCOPE_API_KEY={os.environ['DASHSCOPE_API_KEY']}\n"
            elif os.getenv('OPENAI_API_KEY'):
                config_content += f"OPENAI_API_KEY={os.environ['OPENAI_API_KEY']}\n"
            elif os.getenv('ZHIPUAI_API_KEY'):
                config_content += f"ZHIPUAI_API_KEY={os.environ['ZHIPUAI_API_KEY']}\n"
            elif os.getenv('DEEPSEEK_API_KEY'):
                config_content += f"DEEPSEEK_API_KEY={os.environ['DEEPSEEK_API_KEY']}\n"
                
            config_content += f"""
# MCP服务器配置
MCP_SERVER_URL={server_url}

# 其他配置
LOG_LEVEL=INFO
HTTP_TIMEOUT=30
MAX_RETRIES=3
"""
            
            config_file = Path(__file__).parent / "config.env"
            config_file.write_text(config_content, encoding='utf-8')
            print(f"✅ 配置已保存到 {config_file.name}")
        except Exception as e:
            print(f"⚠️  保存配置文件失败: {e}")
    
    return True


async def test_mcp_server_connection():
    """
    函数名称：test_mcp_server_connection
    功能描述：测试MCP服务器HTTP/SSE连接
    参数说明：无
    返回值：bool，MCP服务器连接是否成功
    """
    print("\n=== MCP服务器连接测试 ===")
    
    try:
        import httpx
        mcp_server_url = os.getenv('MCP_SERVER_URL', 'http://localhost:8000')
        
        async with httpx.AsyncClient() as client:
            # 测试服务器基本连接（不测试SSE端点，因为它是持续连接）
            response = await client.get(f"{mcp_server_url}/", timeout=3.0)
            # 任何响应状态码都表示服务器在运行（包括404）
            if response.status_code in [200, 404, 405]:
                print(f"✅ MCP服务器运行正常 ({mcp_server_url})")
                print(f"✅ 服务器响应状态码: {response.status_code}")
                return True
            else:
                print(f"⚠️ MCP服务器响应异常: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ MCP服务器连接失败: {type(e).__name__}: {str(e)}")
        import traceback
        print("详细错误信息:")
        traceback.print_exc()
        print("请确保:")
        print("1. MCP服务器正在运行")
        print("2. 服务器运行在正确端口 (默认8000)")
        print("3. 网络连接正常")
        return False


async def test_qt_application_connection():
    """
    函数名称：test_qt_application_connection
    功能描述：测试Qt应用程序TCP连接
    参数说明：无
    返回值：bool，Qt应用连接是否成功
    """
    print("\n=== Qt应用连接测试 ===")
    
    try:
        import asyncio
        qt_port = 8088  # Qt应用固定端口
        host = 'localhost'
        
        # 测试TCP连接
        try:
            reader, writer = await asyncio.open_connection(host, qt_port)
            
            # 发送简单的状态查询命令
            message = {
                "id": "test_connection",
                "method": "execute", 
                "params": {"command": "getstate"}
            }
            
            import json
            message_str = json.dumps(message) + '\n'
            writer.write(message_str.encode('utf-8'))
            await writer.drain()
            
            # 接收响应（设置超时）
            response_line = await asyncio.wait_for(reader.readline(), timeout=5.0)
            response_str = response_line.decode('utf-8').strip()
            
            # 关闭连接
            writer.close()
            await writer.wait_closed()
            
            if response_str:
                print(f"✅ Qt应用连接成功 (端口 {qt_port})")
                print(f"✅ Qt应用响应正常")
                return True
            else:
                print(f"⚠️ Qt应用连接成功但无响应")
                return False
                
        except asyncio.TimeoutError:
            print(f"❌ Qt应用连接超时 (端口 {qt_port})")
            return False
        except ConnectionRefusedError:
            print(f"❌ Qt应用连接被拒绝 (端口 {qt_port})")
            print("   请确保Qt应用正在运行")
            return False
            
    except Exception as e:
        print(f"❌ Qt应用连接测试失败: {e}")
        print("请确保:")
        print("1. Qt应用正在运行并监听端口8088")
        print("2. 没有防火墙阻止连接")
        print("3. 端口没有被其他程序占用")
        return False


async def test_mcp_server_availability():
    """
    函数名称：test_mcp_server_availability
    功能描述：测试MCP服务器可用性
    参数说明：无
    返回值：bool，MCP服务器是否可用
    """
    print("\n=== MCP服务器检查 ===")
    
    try:
        # 检查MCP服务器文件是否存在
        import sys
        from pathlib import Path
        
        # 尝试几个可能的MCP服务器位置
        possible_paths = [
            Path(__file__).parent.parent / "mcp-server-qt" / "main.py",
            Path("../mcp-server-qt/main.py"),
            Path("../../Mcp/mcp-server-qt/main.py"),
        ]
        
        mcp_server_found = False
        for mcp_path in possible_paths:
            if mcp_path.exists():
                print(f"✅ 找到MCP服务器: {mcp_path}")
                mcp_server_found = True
                break
        
        if not mcp_server_found:
            print("⚠️ 未找到MCP服务器文件")
            print("   MCP服务器应该独立运行，通过Cursor或其他MCP客户端调用")
            
        # 检查FastMCP是否可用
        try:
            import fastmcp
            print(f"✅ FastMCP可用 (版本: {getattr(fastmcp, '__version__', '未知')})")
        except ImportError:
            print("❌ FastMCP未安装")
            return False
            
        print("💡 MCP服务器信息:")
        print("   - MCP服务器使用stdio通信，不提供HTTP端点")
        print("   - 请确保在Cursor或其他MCP客户端中正确配置")
        print("   - Qt应用程序运行在TCP端口8088")
        
        return True
        
    except Exception as e:
        print(f"❌ MCP服务器检查失败: {e}")
        return False


def print_usage_guide():
    """
    函数名称：print_usage_guide
    功能描述：打印使用指南
    参数说明：无
    返回值：无
    """
    print("\n" + "="*50)
    print("🎯 QT应用控制助手使用指南")
    print("="*50)
    print()
    print("📝 支持的自然语言指令:")
    print("  • 登录账号 <用户名> <密码>")
    print("  • 点击测试按钮")
    print("  • 查看应用状态")
    print("  • 获取当前状态")
    print("  • 退出 (quit/exit/退出)")
    print()
    print("💡 使用技巧:")
    print("  • 直接用中文描述你想要的操作")
    print("  • 系统会自动识别并执行相应的QT控制")
    print("  • 支持多轮对话，可以连续执行操作")
    print()
    print("🔧 如遇问题:")
    print("  • 检查QT应用是否正在运行")
    print("  • 检查MCP服务器连接状态")
    print("  • 查看终端日志信息")
    print("="*50)


async def main():
    """
    函数名称：main
    功能描述：主启动函数
    参数说明：无
    返回值：无
    """
    print("🚀 QT应用控制 MCP 客户端启动器")
    print("="*40)
    
    # 检查依赖
    if not check_dependencies():
        return 1
    
    # 加载配置文件
    load_config()
    
    # 检查环境变量
    if not check_environment():
        print("\n需要配置环境变量...")
        if not setup_environment():
            return 1
    
    # 测试MCP服务器和Qt应用连接
    mcp_ok = await test_mcp_server_connection()
    qt_ok = await test_qt_application_connection()
    
    print("\n=== 连接测试总结 ===")
    print(f"MCP服务器: {'✅ 正常' if mcp_ok else '❌ 异常'}")
    print(f"Qt应用程序: {'✅ 正常' if qt_ok else '❌ 异常'}")
    
    if not mcp_ok:
        print("\n❌ MCP服务器连接失败")
        print("💡 请先启动MCP服务器：")
        print("   cd ../mcp-server-qt && python main.py")
        choice = input("是否仍要继续启动客户端? (y/n): ").lower().strip()
        if choice != 'y':
            print("启动取消")
            return 1
    elif not qt_ok:
        print("\n⚠️ Qt应用连接失败，但MCP服务器正常")
        print("💡 说明：客户端会通过MCP服务器与Qt应用通信")
        print("   请确保Qt应用正在运行")
        choice = input("是否继续启动客户端? (y/n, 默认y): ").lower().strip()
        if choice == 'n':
            print("启动取消")
            return 1
    
    # 打印使用指南
    print_usage_guide()
    
    # 启动主程序
    try:
        print("正在启动 MCP 客户端...")
        
        # 导入主程序
        from main import main as run_main
        await run_main()
        
    except KeyboardInterrupt:
        print("\n用户中断，程序退出")
        return 0
    except Exception as e:
        print(f"\n启动失败: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(0) 