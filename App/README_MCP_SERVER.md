# MCP Qt控制服务器

一个基于MCP (Model Context Protocol) 的Python服务器，用于连接MCP客户端和Qt应用，实现远程控制Qt界面的功能。

## 🎯 项目概述

**架构图：**
```
MCP客户端 ←--stdio/JSON-RPC--→ MCP Python服务器 ←--TCP:8088--→ Qt应用
   ↓                              ↓                     ↓
Claude/Cline                    中间层转换             GUI操作执行
```

## 🚀 功能特性

- **🔌 MCP协议支持**: 完全兼容MCP标准，支持stdio通信
- **📱 Qt应用控制**: 通过TCP连接控制Qt应用界面
- **🛠️ 工具集成**: 提供登录、测试按钮、状态查询等工具
- **🔄 自动重连**: 智能连接管理和错误恢复
- **📝 详细日志**: 完整的调试和监控日志
- **⚡ 异步处理**: 高性能异步架构

## 📁 文件结构

```
mcp_server/
├── mcp_server.py           # 主MCP服务器
├── qt_client.py            # Qt TCP客户端
├── start_server.py         # 启动脚本
├── test_mcp_client.py      # 测试客户端
├── requirements.txt        # Python依赖
├── MCP_CLIENT_CONFIG.md    # 客户端配置指南
└── README_MCP_SERVER.md    # 本文档
```

## 🔧 安装和设置

### 1. 环境要求
- Python 3.8+
- Qt应用运行并监听8088端口

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 测试连接
```bash
# 测试Qt连接
python qt_client.py

# 测试MCP服务器
python start_server.py
```

## 🎮 使用方法

### 快速启动

1. **启动Qt应用** (确保监听8088端口)
2. **启动MCP服务器**:
   ```bash
   python start_server.py
   ```
3. **配置MCP客户端** (见下文配置部分)

### 命令行测试

```bash
# 自动测试
python test_mcp_client.py

# 交互模式测试
python test_mcp_client.py --interactive
```

## 🛠️ 可用工具

### 1. login - 登录工具
**功能**: 执行Qt应用登录操作  
**参数**:
- `account` (string): 用户账号
- `password` (string): 用户密码

**示例**:
```python
await client.call_tool("login", {
    "account": "admin",
    "password": "123456"
})
```

### 2. test_button - 测试按钮
**功能**: 点击Qt应用测试按钮  
**参数**: 无

**示例**:
```python
await client.call_tool("test_button", {})
```

### 3. get_state - 获取状态
**功能**: 获取Qt应用当前状态  
**参数**: 无

**示例**:
```python
await client.call_tool("get_state", {})
```

## 📋 MCP客户端配置

### Claude Desktop 配置

在配置文件中添加：

```json
{
  "mcpServers": {
    "qt-control": {
      "command": "python",
      "args": ["C:\\path\\to\\your\\mcp_server.py"],
      "env": {
        "QT_HOST": "localhost",
        "QT_PORT": "8088"
      }
    }
  }
}
```

**配置文件位置：**
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

### Cline (VS Code插件) 配置

```json
{
  "cline.mcpServers": {
    "qt-control": {
      "command": "python",
      "args": ["C:\\path\\to\\your\\mcp_server.py"]
    }
  }
}
```

### 其他MCP客户端

参考 [MCP_CLIENT_CONFIG.md](MCP_CLIENT_CONFIG.md) 了解详细配置方法。

## 🔍 API文档

### MCP服务器接口

```python
class McpQtServer:
    def __init__(self):
        """初始化MCP服务器"""
    
    async def run(self):
        """运行MCP服务器"""
```

### Qt客户端接口

```python
class QtClient:
    def __init__(self, host="localhost", port=8088):
        """初始化Qt客户端"""
    
    async def send_command(self, command: str) -> dict:
        """发送命令到Qt应用"""
    
    async def send_login_command(self, account: str, password: str) -> dict:
        """发送登录命令"""
    
    async def send_test_button_command(self) -> dict:
        """发送测试按钮命令"""
    
    async def send_get_state_command(self) -> dict:
        """发送获取状态命令"""
```

## 🧪 测试

### 自动化测试
```bash
python test_mcp_client.py
```

### 交互式测试
```bash
python test_mcp_client.py --interactive

> login admin 123456
> test
> state
> quit
```

### 单元测试
```bash
# 测试Qt连接
python qt_client.py

# 测试启动检查
python start_server.py
```

## 🔍 故障排除

### 常见问题

**❌ MCP服务器启动失败**
```
解决方案：
1. 检查Python依赖: pip install -r requirements.txt
2. 确保Qt应用正在运行
3. 检查端口8088是否被占用
4. 查看错误日志
```

**❌ 无法连接Qt应用**
```
解决方案：
1. 确认Qt应用监听8088端口
2. 检查防火墙设置
3. 尝试telnet localhost 8088测试
4. 查看Qt应用控制台输出
```

**❌ 工具调用超时**
```
解决方案：
1. 重启Qt应用
2. 重启MCP服务器  
3. 检查网络连接
4. 查看详细日志
```

### 调试模式

启用详细日志：
```bash
export PYTHONPATH=.
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
" start_server.py
```

### 日志输出

MCP服务器会输出以下日志：
- `🚀 MCP服务器已启动` - 服务器启动成功
- `✅ Qt应用连接正常` - Qt连接测试通过
- `🔧 调用工具: login` - 工具调用记录
- `❌ 连接失败` - 连接错误信息

## 🔧 开发扩展

### 添加新工具

1. **在 `mcp_server.py` 中添加工具处理器：**
```python
@self.server.call_tool()
async def new_tool(arguments: dict) -> list[types.TextContent]:
    # 实现新工具逻辑
    pass
```

2. **在工具列表中注册：**
```python
types.Tool(
    name="new_tool",
    description="新工具描述", 
    inputSchema={...}
)
```

3. **在 `qt_client.py` 中添加对应方法：**
```python
async def send_new_tool_command(self, params) -> Dict[str, Any]:
    return await self.send_command(f"newtool:{params}")
```

### 自定义配置

支持环境变量配置：
- `QT_HOST`: Qt应用主机地址 (默认: localhost)
- `QT_PORT`: Qt应用端口 (默认: 8088)
- `LOG_LEVEL`: 日志级别 (默认: INFO)

```python
import os
host = os.getenv("QT_HOST", "localhost")
port = int(os.getenv("QT_PORT", "8088"))
```

## 📚 相关文档

- [MCP官方文档](https://modelcontextprotocol.io/)
- [Qt应用README](../README.md)
- [客户端配置指南](MCP_CLIENT_CONFIG.md)

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支: `git checkout -b feature/new-feature`
3. 提交更改: `git commit -m 'Add new feature'`
4. 推送分支: `git push origin feature/new-feature`
5. 创建Pull Request

## 📄 许可证

MIT License

## 🆘 支持

如果遇到问题：
1. 查看 [故障排除](#-故障排除) 部分
2. 检查Qt应用和MCP服务器日志
3. 运行测试客户端验证功能
4. 创建Issue报告问题

---

**⚠️ 注意**: 
1. 确保Qt应用先启动，再启动MCP服务器
2. MCP客户端配置路径要使用绝对路径
3. Windows路径使用双反斜杠或正斜杠
4. 测试时建议先用交互模式验证功能 