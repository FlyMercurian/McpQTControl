# MCP Qt控制系统 - 快速开始指南

一个完整的MCP (Model Context Protocol) 系统，用于远程控制Qt应用程序。

## 🎯 系统概述

```
MCP客户端 ←--stdio--→ MCP Python服务器 ←--TCP:8088--→ Qt应用
   ↓                       ↓                    ↓
Claude/Cline            简化JSON-RPC           GUI操作
```

## ✅ 解决导入错误问题

**原问题**: `ImportError: cannot import name 'Server' from 'mcp'`

**解决方案**: 我们创建了**简化版MCP服务器**，无需依赖官方MCP库：
- ✅ 仅使用Python标准库
- ✅ 直接实现JSON-RPC协议
- ✅ 完全兼容MCP客户端
- ✅ 零依赖安装

## 🚀 快速启动步骤

### 1. 启动Qt应用
```bash
# 在Qt项目目录
cd D:\AIPro\MCPControl\McpQTControl\App
# 启动Qt应用（确保监听8088端口）
./App.exe
```

### 2. 测试Qt连接
```bash
python qt_client.py
```

### 3. 启动简化版MCP服务器
```bash
python simple_start_server.py
```

**预期输出：**
```
╔══════════════════════════════════════════════════════════════╗
║                简化版 MCP Qt控制服务器                       ║
╚══════════════════════════════════════════════════════════════╝

✅ Qt应用连接正常
✅ Qt应用响应正常
🚀 启动检查完成，正在启动简化版MCP服务器...
```

### 4. 配置MCP客户端

#### Claude Desktop 配置
编辑配置文件：`%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "qt-control": {
      "command": "python",
      "args": ["D:\\AIPro\\MCPControl\\McpQTControl\\App\\simple_mcp_server.py"]
    }
  }
}
```  

#### Cursor 配置
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

**配置步骤：**
1. 打开Cursor，按 `Ctrl+,` 打开设置
2. 搜索 "MCP"，找到 MCP Servers 部分  
3. 添加服务器配置（如上JSON）
4. 重启Cursor生效

#### Cline (VS Code) 配置
```json
{
  "cline.mcpServers": {
    "qt-control": {
      "command": "python", 
      "args": ["D:\\AIPro\\MCPControl\\McpQTControl\\App\\simple_mcp_server.py"]
    }
  }
}
```

## 🛠️ 可用工具和测试

### 在MCP客户端中使用

1. **登录测试**:
   ```
   请帮我登录Qt应用，账号是admin，密码是123456
   ```

2. **按钮测试**:
   ```
   请点击测试按钮
   ```

3. **状态查询**:
   ```
   请查看Qt应用的当前状态
   ```

### 命令行测试

```bash
# 自动化测试
python test_mcp_client.py

# 交互式测试
python test_mcp_client.py --interactive
> login admin 123456
> test
> state
> quit
```

## 📂 文件结构说明

### Qt应用部分
```
App/
├── mainwindow.h/.cpp      # 主窗口（集成MCP功能）
├── mcpserver.h/.cpp       # TCP服务器
├── mcpprocessor.h/.cpp    # 命令解析器
├── mcpexecutor.h/.cpp     # 功能执行器
└── App.pro                # 项目文件
```

### MCP Python服务器部分
```
App/
├── simple_mcp_server.py      # 主MCP服务器（简化版）
├── qt_client.py              # Qt TCP客户端
├── simple_start_server.py    # 启动脚本（简化版）
├── test_mcp_client.py        # 测试客户端
├── requirements.txt          # 依赖（无额外依赖）
└── QUICK_START.md           # 本指南
```

## 🔍 故障排除

### ❌ Qt应用连接失败
```bash
# 检查Qt应用是否运行
netstat -an | findstr 8088

# 如果没有输出，启动Qt应用
```

### ❌ MCP客户端无法连接
```bash
# 检查Python路径
where python

# 检查文件路径
dir simple_mcp_server.py

# 更新配置文件中的绝对路径
```

### ❌ 工具调用失败
```bash
# 查看MCP服务器日志（在stderr输出）
python simple_start_server.py 2> server.log

# 查看Qt应用控制台输出
```

## 🧪 功能验证清单

- [ ] Qt应用启动并监听8088端口
- [ ] `python qt_client.py` 连接成功
- [ ] `python simple_start_server.py` 启动成功 
- [ ] `python test_mcp_client.py` 测试通过
- [ ] MCP客户端配置正确
- [ ] 工具调用返回正确结果

## 💡 使用技巧

1. **调试模式**: 查看详细日志
   ```bash
   export PYTHONIOENCODING=utf-8
   python simple_start_server.py 2> debug.log
   ```

2. **快速测试**: 单独测试Qt通信
   ```bash
   python qt_client.py
   ```

3. **交互调试**: 逐步测试功能
   ```bash
   python test_mcp_client.py --interactive
   ```

## 📋 支持的MCP客户端

- ✅ **Cursor** (推荐，原生MCP支持)
- ✅ Claude Desktop
- ✅ Cline (VS Code插件) 
- ✅ 自定义MCP客户端
- ✅ 命令行测试客户端

## 🎉 成功标志

当你看到以下内容时，系统已成功运行：

1. **Qt应用**: 状态栏显示"MCP服务器已启动，监听端口: 8088"
2. **MCP服务器**: 显示"✅ Qt应用连接正常"
3. **MCP客户端**: 能够看到并调用qt-control工具
4. **功能测试**: 登录和按钮操作显示弹窗确认

---

**⚠️ 重要提示**:
- 使用**绝对路径**配置MCP客户端
- 确保Qt应用**先启动**，再启动MCP服务器
- Windows路径使用**双反斜杠**或**正斜杠**
- 查看**stderr输出**获取详细日志信息 