# MCP客户端配置指南

本文档说明如何配置MCP客户端来连接Qt控制服务器。

## 🎯 概述

**架构流程：**
```
MCP客户端 ←--stdio--→ MCP Qt服务器 ←--TCP:8088--→ Qt应用
```

## 🔧 环境准备

### 1. 安装Python依赖
```bash
pip install -r requirements.txt
```

### 2. 启动Qt应用
确保Qt应用正在运行并监听8088端口。

### 3. 测试MCP服务器
```bash
python simple_start_server.py
```

## 📋 MCP客户端配置

### Claude Desktop 配置

在 `claude_desktop_config.json` 中添加：

```json
{
  "mcpServers": {
    "qt-control": {
      "command": "python",
      "args": ["/path/to/your/simple_mcp_server.py"],
      "env": {
        "QT_HOST": "localhost",
        "QT_PORT": "8088"
      }
    }
  }
}
```

**配置路径：**
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### Cursor 配置

#### 方法1: 通过设置界面
1. 打开Cursor
2. 按 `Ctrl+,` (Windows) 或 `Cmd+,` (Mac) 打开设置
3. 搜索 "MCP" 或 "Model Context Protocol"
4. 在 MCP Servers 部分添加：
   ```
   Name: qt-control
   Command: python
   Args: D:\AIPro\MCPControl\McpQTControl\App\simple_mcp_server.py
   ```

#### 方法2: 通过配置文件
在 Cursor 设置文件中添加：

```json
{
  "cursor.mcpServers": {
    "qt-control": {
      "command": "python",
      "args": ["D:\\AIPro\\MCPControl\\McpQTControl\\App\\simple_mcp_server.py"]
    }
  }
}
```

**配置文件位置：**
- **Windows**: `%APPDATA%\Cursor\User\settings.json`
- **macOS**: `~/Library/Application Support/Cursor/User/settings.json`
- **Linux**: `~/.config/Cursor/User/settings.json`

### Cline (VS Code插件) 配置

在VS Code设置中添加：

```json
{
  "cline.mcpServers": {
    "qt-control": {
      "command": "python",
      "args": ["/path/to/your/simple_mcp_server.py"]
    }
  }
}
```

### 自定义MCP客户端配置

如果使用自定义MCP客户端，配置示例：

```python
import asyncio
from mcp import ClientSession, StdioServerParameters

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["/path/to/your/simple_mcp_server.py"]
    )
    
    async with ClientSession(server_params) as session:
        # 初始化
        await session.initialize()
        
        # 列出可用工具
        tools = await session.list_tools()
        print("可用工具:", [tool.name for tool in tools])
        
        # 调用工具
        result = await session.call_tool("login", {
            "account": "admin",
            "password": "123456"
        })
        print("登录结果:", result)

if __name__ == "__main__":
    asyncio.run(main())
```

## 🛠️ 可用工具

### 1. login (登录)
**功能**: 登录到Qt应用  
**参数**: 
- `account` (string): 用户账号
- `password` (string): 用户密码

**示例**:
```
请帮我登录Qt应用，账号是admin，密码是123456
```

### 2. test_button (测试按钮)
**功能**: 点击Qt应用的测试按钮  
**参数**: 无

**示例**:
```
请点击测试按钮
```

### 3. get_state (获取状态)
**功能**: 获取Qt应用当前状态  
**参数**: 无

**示例**:
```
请查看Qt应用的当前状态
```

## 🔍 故障排除

### 常见问题

**Q: MCP服务器启动失败**
```
A: 检查以下项目：
   1. Python依赖是否安装完整
   2. Qt应用是否在运行
   3. 端口8088是否被占用
   4. 网络连接是否正常
```

**Q: 工具调用超时**
```
A: 可能原因：
   1. Qt应用响应慢
   2. 网络延迟
   3. Qt应用异常
   
   解决方案：
   1. 重启Qt应用
   2. 检查Qt应用日志
   3. 重启MCP服务器
```

**Q: 登录失败**
```
A: 检查：
   1. 账号密码格式是否正确
   2. Qt应用登录逻辑是否正常
   3. 查看Qt应用界面确认状态
```

### 调试模式

启用详细日志：
```bash
export PYTHONPATH=.
python -c "import logging; logging.basicConfig(level=logging.DEBUG)" start_server.py
```

### 测试连接

单独测试Qt连接：
```bash
python qt_client.py
```

## 📝 配置模板

### 完整配置模板 (Claude Desktop)

```json
{
  "mcpServers": {
    "qt-control": {
      "command": "python",
      "args": [
        "C:\\path\\to\\your\\mcp_server.py"
      ],
      "env": {
        "QT_HOST": "localhost",
        "QT_PORT": "8088",
        "LOG_LEVEL": "INFO"
      }
    }
  },
  "globalShortcut": "Ctrl+Shift+C"
}
```

### 高级配置

如果Qt应用运行在不同机器：

```json
{
  "mcpServers": {
    "qt-control": {
      "command": "python",
      "args": ["/path/to/your/mcp_server.py"],
      "env": {
        "QT_HOST": "192.168.1.100",
        "QT_PORT": "8088"
      }
    }
  }
}
```

## 🚀 快速开始

1. **启动Qt应用**
2. **安装依赖**: `pip install -r requirements.txt`
3. **测试连接**: `python qt_client.py`
4. **启动MCP服务器**: `python simple_start_server.py` 
5. **配置MCP客户端** (见上面配置部分)
6. **开始使用**: 在MCP客户端中调用工具

## 📞 支持

如果遇到问题，请检查：
1. Qt应用控制台输出
2. MCP服务器日志
3. MCP客户端错误信息

---
**注意**: 确保Qt应用先启动，再启动MCP服务器，最后配置MCP客户端。 