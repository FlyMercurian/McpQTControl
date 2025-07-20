# QT应用控制 MCP 客户端

这是一个基于 fastmcp 的 MCP 客户端，用于控制 QT 应用程序。

## 功能特性

- 🚀 异步 MCP 客户端，支持高并发操作
- 🤖 集成大语言模型，支持自然语言控制
- 🎯 专为 QT 应用控制优化的系统提示词
- 📝 完整的错误处理和日志记录
- 🔧 支持多种 QT 操作：登录、测试按钮、状态查询
- 🛠️ 支持多个 LLM 提供商：阿里云、OpenAI、智谱AI、Deepseek
- ⚙️ 灵活的配置方式：环境文件或系统变量
- 🎭 智能启动脚本，支持配置向导和环境检查

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
MCP_SERVER_URL=http://localhost:8080
```

### 方式二：使用系统环境变量

```bash
# Linux/Mac
export DASHSCOPE_API_KEY="your_dashscope_api_key"
export LLM_MODEL_NAME="qwen-plus-latest"
export LLM_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
export MCP_SERVER_URL="http://localhost:8080"
```

```powershell
# Windows PowerShell
$env:DASHSCOPE_API_KEY="your_dashscope_api_key"
$env:LLM_MODEL_NAME="qwen-plus-latest" 
$env:LLM_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
$env:MCP_SERVER_URL="http://localhost:8080"
```

### 支持的LLM提供商

| 提供商 | API密钥变量 | 默认模型 | 默认URL |
|--------|-------------|----------|---------|
| 阿里云通义千问 | `DASHSCOPE_API_KEY` | `qwen-plus-latest` | `https://dashscope.aliyuncs.com/compatible-mode/v1` |
| OpenAI | `OPENAI_API_KEY` | `gpt-3.5-turbo` | `https://api.openai.com/v1` |
| 智谱AI | `ZHIPUAI_API_KEY` | `glm-4` | `https://open.bigmodel.cn/api/paas/v4` |
| Deepseek | `DEEPSEEK_API_KEY` | `deepseek-chat` | `https://api.deepseek.com/v1` |

## 使用方法

1. **启动 MCP 服务器**（确保你的 QT 控制服务正在运行）

2. **运行 MCP 客户端**：

   **一键启动**（推荐）：
   ```bash
   # Windows
   run.bat
   
   # Linux/Mac
   ./run.sh
   ```
   
   **使用启动脚本**（带环境检查）：
   ```bash
   python start.py
   ```
   
   **直接启动**：
   ```bash
   python main.py
   ```

3. **首次运行配置向导**：
   - 启动脚本会自动检查依赖和配置
   - 如果未配置，会引导你完成配置设置
   - 支持选择不同的 LLM 提供商
   - 可选择保存配置到 `config.env` 文件

4. **使用自然语言控制 QT 应用**：

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

## 故障排除

### 连接问题
```
Error: Not connected to MCP server
```
**解决方案**: 检查 MCP 服务器是否运行，端口是否正确

### API 密钥问题
```
请设置环境变量 DASHSCOPE_API_KEY
```
**解决方案**: 设置正确的阿里云 API 密钥

### 工具执行失败
```
工具执行错误: ...
```
**解决方案**: 检查 QT 应用程序状态，查看服务器日志 