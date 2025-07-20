# FastMCP Qt控制服务器

基于 **FastMCP** 框架的Qt应用程序控制服务器，提供通过MCP协议远程控制Qt应用的功能。

## 🚀 功能特性

- ✅ **登录控制**: 通过MCP命令执行Qt应用登录操作
- ✅ **按钮控制**: 远程点击Qt应用的测试按钮
- ✅ **状态查询**: 获取Qt应用的实时状态信息
- ✅ **Cursor集成**: 完美支持Cursor MCP客户端
- ✅ **自然语言**: 使用自然语言与AI助手交互控制Qt应用

## 📋 系统要求

- **Python**: 3.8+ 
- **Qt应用**: 需要运行在localhost:8088端口
- **FastMCP**: 已配置好的FastMCP环境
- **Cursor**: 支持MCP的Cursor客户端

## 🔧 安装配置

### 1. 环境准备

确保已安装FastMCP依赖：
```bash
pip install mcp fastmcp
```

### 2. 启动Qt应用

确保Qt应用正在运行并监听8088端口：
```bash
# 在Qt项目目录中编译并运行
qmake App.pro
make
./App  # Linux/macOS
# 或双击 App.exe (Windows)
```

### 3. 测试MCP服务器

```bash
cd mcp-server-qt
python main.py
```

正常输出应该显示：
```
INFO:__main__:测试Qt应用连接...
INFO:__main__:📊 Qt应用原始响应: {...}
INFO:__main__:✅ Qt应用连接正常 (JSON-RPC格式)
```

## 🔑 Cursor MCP客户端配置

### 方法一：通过Cursor设置界面配置

1. **打开Cursor设置**
   - 按 `Ctrl+,` (Windows/Linux) 或 `Cmd+,` (macOS)
   - 或者点击菜单：File → Preferences → Settings

2. **搜索MCP设置**
   - 在设置搜索框中输入 "mcp"
   - 找到 "Cursor: Mcp Servers" 设置项

3. **添加Qt控制服务器**
   ```
   Server Name: qt-control
   Command: python
   Arguments: D:\AIPro\MCPControl\McpQTControl\App\mcp-server-qt\main.py
   ```

   > **注意**: 请将路径替换为你的实际项目路径

### 方法二：直接编辑配置文件

1. **打开Cursor设置文件**
   
   Windows: `%APPDATA%\Cursor\User\settings.json`
   macOS: `~/Library/Application Support/Cursor/User/settings.json`
   Linux: `~/.config/Cursor/User/settings.json`

2. **添加MCP服务器配置**
   ```json
    "qt-control": {
      "command": "python",
      "args": ["D:\\AIPro\\MCPControl\\McpQTControl\\Mcp\\mcp-server-qt\\main.py"],
      "env": {
        "PYTHONIOENCODING": "utf-8"
      }
    }
   ```

3. **保存并重启Cursor**

## 💡 使用方法

配置完成后，你可以在Cursor中与AI助手进行自然语言对话来控制Qt应用：

### 登录操作
```
你: 请帮我登录Qt应用，账号是admin，密码是123456
AI: 好的，我来帮你登录Qt应用...
    [调用login工具]
    登录结果: ✅ 成功
    消息: 登录成功
```

### 按钮控制
```
你: 请点击测试按钮
AI: 好的，我来点击测试按钮...
    [调用test_button工具]
    测试按钮结果: ✅ 成功
    消息: 按钮点击成功
```

### 状态查询
```
你: 请查看Qt应用的当前状态
AI: 让我查看Qt应用的状态...
    [调用get_state工具]
    状态查询结果: ✅ 成功
    详细信息: {
      "applicationVersion": "",
      "currentTime": "周日 1月 19 12:00:00 2025",
      "isEnabled": true,
      "isVisible": true,
      "windowTitle": "MCP Qt Control Application"
    }
```

## 🛠️ 可用MCP工具

| 工具名称 | 参数 | 功能描述 |
|---------|------|----------|
| `login` | account, password | 执行Qt应用登录操作 |
| `test_button` | 无 | 点击Qt应用测试按钮 |
| `get_state` | 无 | 获取Qt应用状态信息 |

## 🔍 故障排除

### 1. 连接问题

**问题**: `WARNING:__main__:⚠️ Qt应用连接可能有问题`

**解决方案**:
```bash
# 检查Qt应用是否运行
netstat -an | findstr :8088

# 确认Qt应用日志
# 查看Qt应用控制台输出

# 测试TCP连接
telnet localhost 8088
```

### 2. MCP工具错误

**问题**: `RuntimeError: asyncio.run() cannot be called from a running event loop`

**原因**: 这是测试脚本的问题，实际MCP使用中不会出现

**解决方案**: 在Cursor中正常使用，不要直接导入测试工具

### 3. 路径配置错误

**问题**: Cursor无法找到MCP服务器

**解决方案**:
```bash
# 确认文件存在
dir "D:\AIPro\MCPControl\McpQTControl\App\mcp-server-qt\main.py"

# 使用绝对路径
"args": ["C:\\Python311\\python.exe", "D:\\AIPro\\...\\main.py"]
```

### 4. Python环境问题

**问题**: 导入模块失败

**解决方案**:
```bash
# 检查Python版本
python --version

# 检查FastMCP安装
python -c "import mcp.server.fastmcp; print('FastMCP已安装')"

# 重新安装依赖
pip install --upgrade mcp fastmcp
```

## 📝 开发说明

### 项目结构
```
mcp-server-qt/
├── main.py           # FastMCP服务器主程序
├── README.md         # 本文档
└── ...              # 其他配置文件
```

### 核心组件

- **QtClient**: TCP客户端，负责与Qt应用通信
- **MCP Tools**: 登录、按钮、状态查询三个核心工具
- **MCP Resources**: 服务器状态资源
- **MCP Prompts**: 交互提示模板

### 扩展开发

如需添加新的控制功能，可以：

1. 在Qt应用中添加新的命令处理
2. 在`main.py`中添加对应的MCP工具：

```python
@mcp.tool()
def new_function(param: str) -> str:
    """新功能描述"""
    async def _new_function():
        response = await qt_client.send_command(f"newcmd:{param}")
        return format_qt_response(response, "新功能")
    
    return asyncio.run(_new_function())
```

## 🎯 使用技巧

1. **自然语言交互**: 用描述性语言而非技术命令
2. **错误处理**: AI会自动处理错误并提供建议
3. **状态确认**: 操作前后可以查询状态确认
4. **批量操作**: 可以要求AI执行多个连续操作

## 📞 支持联系

如有问题或建议，请：
- 查看Qt应用日志
- 检查MCP服务器输出
- 确认网络连接状态
- 验证配置文件正确性

---

**享受通过自然语言控制Qt应用的便捷体验！** 🎉
