# Cursor MCP配置教程

本教程将指导你在Cursor中配置MCP Qt控制服务器，实现通过AI助手远程控制Qt应用的功能。

## 🎯 为什么选择Cursor？

- ✅ **原生MCP支持**: Cursor内置了MCP协议支持
- ✅ **配置简单**: 通过UI界面或配置文件轻松配置
- ✅ **实时交互**: 可以直接与AI助手对话控制Qt应用
- ✅ **开发友好**: 基于VS Code，熟悉的界面和快捷键

## 🚀 配置步骤

### 前置准备

1. **确保Qt应用正在运行**
   ```bash
   # 在Qt项目目录启动应用
   cd D:\AIPro\MCPControl\McpQTControl\App
   ./App.exe
   ```

2. **测试MCP服务器**
   ```bash
   cd mcp-server-qt
   python main.py
   ```

### 方法1: 通过Cursor设置界面配置

1. **打开Cursor设置**
   - 快捷键: `Ctrl+,` (Windows) 或 `Cmd+,` (Mac)
   - 或者通过菜单: File → Preferences → Settings

2. **搜索MCP设置**
   - 在设置搜索框中输入: `MCP` 或 `Model Context Protocol`
   - 找到 "MCP Servers" 相关设置

3. **添加Qt控制服务器**
   ```
   Server Name: qt-control
   Command: python
   Arguments: D:\AIPro\MCPControl\McpQTControl\App\mcp-server-qt\main.py
   ```

4. **保存并重启Cursor**

### 方法2: 通过配置文件配置

1. **找到配置文件**
   
   **Windows**:
   ```
   %APPDATA%\Cursor\User\settings.json
   ```
   
   **macOS**:
   ```
   ~/Library/Application Support/Cursor/User/settings.json
   ```
   
   **Linux**:
   ```
   ~/.config/Cursor/User/settings.json
   ```

2. **编辑配置文件**
   
   在 `settings.json` 中添加：
   ```json
   {
     "cursor.mcpServers": {
       "qt-control": {
         "command": "python",
         "args": ["D:\\AIPro\\MCPControl\\McpQTControl\\App\\mcp-server-qt\\main.py"],
         "env": {
           "PYTHONIOENCODING": "utf-8"
         }
       }
     }
   }
   ```

3. **保存文件并重启Cursor**

### 方法3: 通过命令面板配置

1. **打开命令面板**
   - 快捷键: `Ctrl+Shift+P` (Windows) 或 `Cmd+Shift+P` (Mac)

2. **搜索MCP命令**
   - 输入: `MCP: Configure Servers`
   - 选择对应的命令

3. **添加服务器配置**
   - 按照提示添加服务器信息

## 🛠️ 验证配置

### 检查MCP工具是否可用

1. **打开Cursor AI聊天面板**
   - 快捷键: `Ctrl+L` 或点击侧边栏AI图标

2. **查看可用工具**
   
   在聊天框中输入：
   ```
   你有哪些工具可以使用？
   ```
   
   应该能看到：
   - `login` - 登录到Qt应用
   - `test_button` - 点击测试按钮  
   - `get_state` - 获取应用状态

### 功能测试

1. **测试登录功能**
   ```
   请帮我登录Qt应用，账号是admin，密码是123456
   ```

2. **测试按钮功能**
   ```
   请点击测试按钮
   ```

3. **测试状态查询**
   ```
   请查看Qt应用的当前状态
   ```

## 🔍 故障排除

### ❌ 找不到MCP设置选项

**原因**: Cursor版本可能不支持MCP或设置界面有所不同

**解决方案**:
1. 更新Cursor到最新版本
2. 使用配置文件方法
3. 查看Cursor官方文档确认设置位置

### ❌ 工具不显示或调用失败

**原因**: 路径配置错误或Python环境问题

**解决方案**:
1. **检查路径**
   ```bash
   # 确认文件存在
   dir D:\AIPro\MCPControl\McpQTControl\App\mcp-server-qt\main.py
   ```

2. **检查Python命令**
   ```bash
   # 确认python可用
   python --version
   where python
   ```

3. **使用绝对路径**
   ```json
   {
     "cursor.mcpServers": {
       "qt-control": {
         "command": "C:\\Python311\\python.exe",
         "args": ["D:\\AIPro\\MCPControl\\McpQTControl\\App\\mcp-server-qt\\main.py"]
       }
     }
   }
   ```

### ❌ 连接Qt应用失败

**原因**: Qt应用未启动或端口被占用

**解决方案**:
1. **确认Qt应用运行**
   ```bash
   netstat -an | findstr 8088
   ```

2. **重启Qt应用**
   ```bash
   # 重新启动Qt应用
   ./App.exe
   ```

3. **检查MCP服务器日志**
   ```bash
   python simple_start_server.py 2> debug.log
   type debug.log
   ```

## 💡 使用技巧

### 常用对话示例

```
# 查看应用状态
你好，请帮我查看一下Qt应用的当前状态

# 执行登录
请帮我登录Qt应用，使用这些凭据：用户名admin，密码123456  

# 点击按钮
请点击测试按钮看看

# 组合操作
先帮我查看状态，然后登录（用户名test，密码pass），最后点击测试按钮
```

### 调试技巧

1. **启用详细日志**
   ```json
   {
     "cursor.mcpServers": {
       "qt-control": {
         "command": "python",
         "args": ["simple_mcp_server.py"],
         "env": {
           "PYTHONIOENCODING": "utf-8",
           "LOG_LEVEL": "DEBUG"
         }
       }
     }
   }
   ```

2. **查看连接状态**
   
   在Cursor中按 `F12` 打开开发者工具，查看控制台输出

3. **手动测试**
   ```bash
   # 单独测试MCP服务器
   python test_mcp_client.py --interactive
   ```

## 🎉 完成配置

当你在Cursor中看到以下情况时，说明配置成功：

1. ✅ AI助手能识别qt-control工具
2. ✅ 工具调用返回正确的Qt应用响应  
3. ✅ Qt应用界面显示对应的操作结果（弹窗等）

现在你可以在Cursor中直接与AI助手对话来控制Qt应用了！

---

**💡 提示**: 
- 使用绝对路径避免路径问题
- 确保Python环境变量正确设置
- Qt应用必须先启动才能连接成功
- 遇到问题时查看Cursor开发者工具的控制台输出 