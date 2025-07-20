# QT应用控制 MCP 客户端

基于 FastMCP 的智能 QT 应用控制系统，通过自然语言实现 QT 应用程序的自动化控制。

## 🏗️ 系统架构

```
用户输入 → LLM理解 → MCP客户端 → MCP服务器(SSE) → Qt应用(TCP:8088)
```

- **MCP服务器**: 端口8000，使用SSE传输模式
- **Qt应用**: 端口8088，TCP JSON-RPC通信
- **传输方式**: Server-Sent Events (SSE) 持续连接

## ✨ 功能特性

- 🚀 **异步架构**: FastMCP客户端，支持SSE流式通信
- 🤖 **智能理解**: 集成大语言模型，自然语言转工具调用
- 🎯 **专业优化**: 专为QT应用控制设计的系统提示词
- 📝 **全面日志**: 完整的错误处理和调试信息
- 🔧 **丰富操作**: 登录认证、按钮操作、状态查询等
- 🛠️ **多平台LLM**: 阿里云、OpenAI、智谱AI、Deepseek
- ⚙️ **灵活配置**: 环境文件或系统变量两种方式
- 🎭 **智能启动**: 环境检查、配置向导、连接测试

## 安装依赖

```bash
pip install -r requirements.txt
```

## 环境配置

### 方式一：使用配置文件 (推荐)

编辑 `config.env` 文件设置你的配置：

```bash
# 大语言模型配置 - 选择一个提供商
# 阿里云通义千问 (推荐)
DASHSCOPE_API_KEY=your_dashscope_api_key_here
LLM_MODEL_NAME=qwen-plus-latest
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1

# 或者使用OpenAI
# OPENAI_API_KEY=your_openai_api_key_here
# LLM_MODEL_NAME=gpt-3.5-turbo
# LLM_BASE_URL=https://api.openai.com/v1

# MCP服务器配置
MCP_SERVER_URL=http://localhost:8000
```

### 方式二：使用系统环境变量

```bash
# Linux/Mac
export DASHSCOPE_API_KEY="your_dashscope_api_key"
export LLM_MODEL_NAME="qwen-plus-latest"
export LLM_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export MCP_SERVER_URL="http://localhost:8000"
```

```powershell
# Windows PowerShell
$env:DASHSCOPE_API_KEY="your_dashscope_api_key"
$env:LLM_MODEL_NAME="qwen-plus-latest" 
$env:LLM_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
$env:MCP_SERVER_URL="http://localhost:8000"
```

### 支持的LLM提供商

| 提供商 | API密钥变量 | 默认模型 | 默认URL |
|--------|-------------|----------|---------|
| 阿里云通义千问 | `DASHSCOPE_API_KEY` | `qwen-plus-latest` | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| OpenAI | `OPENAI_API_KEY` | `gpt-3.5-turbo` | `https://api.openai.com/v1` |
| 智谱AI | `ZHIPUAI_API_KEY` | `glm-4` | `https://open.bigmodel.cn/api/paas/v4` |
| Deepseek | `DEEPSEEK_API_KEY` | `deepseek-chat` | `https://api.deepseek.com/v1` |

## ⚡ 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动MCP服务器（新终端）
cd ../mcp-server-qt && python main.py

# 3. 快速启动客户端
python start_simple.py

# 4. 开始对话
用户: 登录账号wyx，密码124
助手: 登录成功！用户 wyx 已成功登录系统
```

## 🚀 使用方法

### 1️⃣ 启动MCP服务器
```bash
cd ../mcp-server-qt
python main.py
```
> 🔵 服务器将在端口8000启动SSE模式，等待客户端连接

### 2️⃣ 启动客户端

**🌟 方式一：完整启动（推荐新用户）**
```bash
python start.py
```
- ✅ 自动检查依赖和配置
- ✅ 测试MCP服务器和Qt应用连接  
- ✅ 配置向导，引导首次设置
- ✅ 详细的启动日志和错误诊断

**⚡ 方式二：快速启动（推荐熟练用户）** 
```bash
python start_simple.py  
```
- ⚡ 跳过连接测试，直接启动
- ⚡ 适用于已知服务器正常运行
- ⚡ 更快的启动速度，减少等待

**🔧 方式三：直接启动（调试模式）**
```bash
python main.py
```
- 🔧 最小化启动，不含任何检查
- 🔧 适用于开发调试和问题排查

### 3️⃣ 首次配置向导
- 启动脚本会自动检查依赖和配置
- 如果未配置，会引导你完成设置
- 支持选择不同的LLM提供商
- 可选保存配置到`config.env`文件

### 4️⃣ 开始控制Qt应用

### 支持的指令示例：

```
用户: 登录账号wyx，密码124
助手: {"tool":"login","arguments":{"account":"wyx","password":"124"}}
助手: 登录成功！用户 wyx 已成功登录系统

用户: 点击测试按钮
助手: {"tool":"test_button","arguments":{"random_string":"test"}}
助手: 测试按钮点击成功！

用户: 查看应用状态
助手: {"tool":"get_state","arguments":{"random_string":"state"}}
助手: 应用当前状态：运行中...

用户: 退出
QT控制助手退出
```

## 代码结构

### MCPClient 类
- `connect_to_server(base_url)`: 连接到 MCP 服务器
- `list_tools()`: 获取可用工具列表
- `execute_tool(tool_name, arguments)`: 执行 MCP 工具
- `cleanup()`: 清理资源

### LLMClient 类
- `__init__(model_name, url, api_key)`: 初始化 LLM 客户端
- `get_response(messages)`: 获取 LLM 响应

### ChatSession 类
- `process_llm_response(response)`: 处理 LLM 响应并执行工具
- `start(system_message)`: 启动对话会话

## 系统提示词特性

专为 QT 应用控制优化：

1. **指令映射**：
   - "登录" → `login` 工具
   - "点击测试按钮" → `test_button` 工具
   - "查看状态" → `get_state` 工具

2. **JSON 格式严格控制**：
   - 禁止 Markdown 标记
   - 纯净 JSON 输出
   - 参数类型验证

3. **友好的中文响应**：
   - 工具执行后自动转换为自然语言
   - 突出关键信息
   - 错误时提供解决建议

## 错误处理

- ✅ 网络连接错误处理
- ✅ MCP 服务器响应错误处理
- ✅ LLM API 调用错误处理
- ✅ JSON 解析错误处理
- ✅ 工具执行错误处理

## 注意事项

1. 确保 MCP 服务器在运行并监听正确端口
2. 确保设置了有效的 `DASHSCOPE_API_KEY`
3. 网络连接正常，能够访问阿里云 API
4. QT 应用程序正在运行并可接受控制

## 🔧 故障排除

### ⚠️ SSE连接超时（正常现象）
```
❌ MCP服务器连接失败: ReadTimeout
测试SSE端点超时
```
**重要说明**: 这是**正常现象**！SSE端点是持续连接，用普通HTTP测试会超时。

**解决方案**: 
- 使用`python start_simple.py`跳过连接测试
- 检查MCP服务器日志确认服务器正在运行
- 基础连接404响应表示服务器正常

### 🔌 MCP服务器连接问题
```
Error: Not connected to MCP server
ConnectionRefusedError
```
**解决方案**: 
1. 确保MCP服务器正在运行: `cd ../mcp-server-qt && python main.py`
2. 检查端口8000是否被占用: `netstat -an | grep 8000`
3. 确认`MCP_SERVER_URL=http://localhost:8000`

### 🔑 API密钥问题
```
❌ 请在config.env文件中设置API密钥
```
**解决方案**: 
- 编辑`config.env`设置正确的API密钥
- 支持的密钥：`DASHSCOPE_API_KEY`, `OPENAI_API_KEY`, `ZHIPUAI_API_KEY`, `DEEPSEEK_API_KEY`

### 🎯 Qt应用连接失败
```
❌ Qt应用连接被拒绝 (端口8088)
```
**解决方案**: 
1. 确保Qt应用正在运行并监听端口8088
2. 检查防火墙设置
3. 验证TCP端口: `telnet localhost 8088`

### ⚙️ 工具执行失败
```
工具执行错误: ...
```
**解决方案**: 
1. 检查Qt应用程序状态
2. 查看MCP服务器日志
3. 验证工具参数格式正确

### 🌐 网络连接问题
```
Error connecting to LLM API
```
**解决方案**: 
1. 检查网络连接
2. 验证API地址可访问
3. 确认API密钥有效且有余额 