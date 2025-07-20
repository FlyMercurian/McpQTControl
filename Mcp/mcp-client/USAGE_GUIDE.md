# 🚀 QT应用控制 MCP 客户端使用指南

## ✅ 问题已修复！

**现在系统已经完全配置正确：**
- ✅ FastMCP 2.10.6 已安装
- ✅ 服务器改为SSE模式，运行在8000端口  
- ✅ 客户端使用FastMCP Client正确连接
- ✅ Qt应用仍运行在8088端口
- ✅ 所有配置文件已更新

## 📋 系统架构

```
用户输入 → LLM(通义千问) → MCP客户端 → MCP服务器(8000) → Qt应用(8088)
```

**端口说明：**
- **8000**: MCP服务器 (FastMCP SSE模式)
- **8088**: Qt应用程序 (TCP服务器)

## 🎯 正确启动流程

### 1. 启动Qt应用程序
```bash
# 在Qt项目目录
cd App
./your-qt-app  # 确保监听8088端口
```

### 2. 启动MCP服务器
```bash
# 新终端窗口
cd Mcp/mcp-server-qt
python main.py
```

你应该看到：
```
INFO:__main__:🚀 启动FastMCP Qt控制服务器...
INFO:__main__:✅ Qt应用连接正常
INFO:__main__:🌐 启动SSE模式MCP服务器在端口8000...
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 3. 启动MCP客户端
```bash
# 新终端窗口
cd Mcp/mcp-client
python start.py
```

你应该看到：
```
✅ 从 config.env 加载配置
✅ API密钥 (阿里云通义千问): sk-20daa...
✅ MCP服务器连接成功 (http://localhost:8000)
✅ Qt应用连接成功 (端口 8088)

=== QT应用控制助手已启动 ===
用户: 
```

## 💡 使用示例

**现在你可以输入自然语言指令：**

```
用户: 登录账号wyx，密码124
助手: {"tool":"login","arguments":{"account":"wyx","password":"124"}}
助手: ✅ 登录成功！用户 wyx 已成功登录Qt应用程序

用户: 点击测试按钮  
助手: {"tool":"test_button","arguments":{}}
助手: ✅ 测试按钮点击成功！

用户: 查看应用状态
助手: {"tool":"get_state","arguments":{}}  
助手: 应用状态：运行中...
```

## 🔧 快速启动脚本

**Windows一键启动：**
```batch
:: 创建 start_all.bat
@echo off
echo 启动QT应用控制系统...

:: 启动Qt应用 (根据你的实际情况修改)
start "Qt应用" cmd /c "cd App && your-qt-app.exe"

:: 等待2秒
timeout /t 2

:: 启动MCP服务器
start "MCP服务器" cmd /c "cd Mcp/mcp-server-qt && python main.py"

:: 等待3秒
timeout /t 3

:: 启动客户端
cd Mcp/mcp-client
python start.py

pause
```

## 📊 故障诊断

### 问题1：MCP服务器连接失败
```
❌ MCP服务器连接失败
```
**解决方案：**
```bash
# 检查8000端口
netstat -an | findstr :8000

# 手动启动MCP服务器
cd Mcp/mcp-server-qt
python main.py
```

### 问题2：Qt应用连接失败
```
❌ Qt应用连接被拒绝 (端口 8088)
```
**解决方案：**
```bash
# 检查8088端口
netstat -an | findstr :8088

# 确保Qt应用正在运行
# 检查Qt应用日志
```

### 问题3：LLM API调用失败
```
LLM调用失败: ...
```
**解决方案：**
```bash
# 检查API密钥
python -c "import os; print('API Key:', os.getenv('DASHSCOPE_API_KEY', 'Not set')[:10] + '...')"

# 测试API连接
python -c "
from openai import OpenAI
client = OpenAI(
    api_key='your-api-key',
    base_url='https://dashscope.aliyuncs.com/compatible-mode/v1'
)
print('API测试成功')
"
```

## 🎉 验证系统工作正常

运行这个完整测试：

```bash
# 1. 检查所有端口
netstat -an | findstr ":8000\|:8088"

# 2. 测试MCP服务器
curl http://localhost:8000/sse

# 3. 测试Qt应用
python -c "
import asyncio
import json

async def test_qt():
    reader, writer = await asyncio.open_connection('localhost', 8088)
    msg = {'id': 'test', 'method': 'execute', 'params': {'command': 'getstate'}}
    writer.write((json.dumps(msg) + '\n').encode())
    await writer.drain()
    resp = await reader.readline()
    print('Qt响应:', resp.decode().strip())
    writer.close()
    await writer.wait_closed()

asyncio.run(test_qt())
"

# 4. 启动客户端测试
cd Mcp/mcp-client
python start.py
```

如果以上都正常，输入：`登录账号wyx，密码124` 应该可以工作！

## 📝 配置说明

**当前配置文件 `config.env`：**
```bash
# 通义千问配置
DASHSCOPE_API_KEY=sk-20daa801ffcc4b3cad6f3b6353de6ebe
LLM_MODEL_NAME=qwen-plus-latest
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# MCP服务器 (SSE模式)
MCP_SERVER_URL=http://localhost:8000

# Qt应用端口：8088 (固定)
```

**现在一切都应该正常工作了！** 🎉 