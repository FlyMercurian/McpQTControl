# MCP Qt Control Application

一个基于Qt的MCP（Model Context Protocol）控制应用，支持通过TCP连接接收外部命令并执行相应的GUI操作。

## 🚀 功能特性

- **TCP服务器**：监听8088端口，接受MCP客户端连接
- **命令解析**：支持JSON-RPC和纯文本两种消息格式
- **登录控制**：通过MCP命令执行用户登录操作
- **按钮控制**：远程触发界面按钮点击
- **状态查询**：获取应用当前运行状态
- **实时反馈**：所有操作都有状态栏和日志反馈

## 📋 系统要求

- Qt 5.12+ 或 Qt 6.x
- C++11 支持
- Windows/Linux/macOS

## 🔧 编译安装

### 1. 克隆代码
```bash
git clone <repository-url>
cd McpQTControl/App
```

### 2. 使用Qt Creator
1. 打开 `App.pro` 文件
2. 配置Qt Kit
3. 点击"构建"按钮

### 3. 命令行编译
```bash
qmake App.pro
make
```

## 🎮 使用方法

### 启动应用
运行编译生成的可执行文件，应用将自动：
- 启动GUI界面
- 在8088端口启动TCP服务器
- 在状态栏显示服务器状态

### MCP命令格式

#### 支持的命令

| 命令 | 格式 | 功能描述 |
|------|------|----------|
| 登录 | `login:账号:密码` | 执行用户登录操作（显示弹窗） |
| 测试按钮 | `testbutton` | 点击测试按钮（显示弹窗） |
| 获取状态 | `getstate` | 获取应用当前状态 |

#### 1. JSON-RPC 格式（推荐）

**登录请求：**
```json
{
    "id": "login_001",
    "method": "execute", 
    "params": {
        "command": "login:admin:123456"
    }
}
```

**测试按钮请求：**
```json
{
    "id": "test_001",
    "method": "execute",
    "params": {
        "command": "testbutton"
    }
}
```

**获取状态请求：**
```json
{
    "id": "state_001", 
    "method": "execute",
    "params": {
        "command": "getstate"
    }
}
```

#### 2. 纯文本格式

直接发送命令字符串：
```
login:admin:123456
testbutton
getstate
```

### 响应格式

**成功响应：**
```json
{
    "id": "login_001",
    "result": {
        "success": true,
        "message": "登录成功", 
        "data": {
            "account": "admin",
            "loginTime": "2024-01-15T10:30:00"
        }
    }
}
```

**失败响应：**
```json
{
    "id": "login_001",
    "error": {
        "code": -1,
        "message": "账号或密码格式无效",
        "data": {}
    }
}
```

## 🛠 测试连接

### 使用telnet测试
```bash
telnet localhost 8088
```

发送测试命令：
```
login:testuser:testpass
testbutton
getstate
```

### 使用Python客户端测试
```python
import socket
import json

def send_mcp_command(command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 8088))
    
    message = {
        "id": "test_001",
        "method": "execute",
        "params": {"command": command}
    }
    
    sock.send((json.dumps(message) + '\n').encode())
    response = sock.recv(1024).decode()
    sock.close()
    
    print(f"发送: {command}")
    print(f"响应: {response}")

# 测试登录
send_mcp_command("login:admin:123456")

# 测试按钮
send_mcp_command("testbutton")

# 获取状态
send_mcp_command("getstate")
```

## 📁 项目结构

```
App/
├── App.pro                 # Qt项目文件
├── main.cpp               # 程序入口
├── mainwindow.h/.cpp      # 主窗口（GUI界面）
├── mainwindow.ui          # UI设计文件
├── mcpserver.h/.cpp       # TCP服务器（网络通信）
├── mcpprocessor.h/.cpp    # 命令解析器
├── mcpexecutor.h/.cpp     # 功能执行器
└── README.md              # 说明文档
```

## 🔍 架构说明

### 核心组件

1. **McpServer** - TCP服务器类
   - 监听客户端连接
   - 接收和发送消息
   - 管理多客户端连接

2. **McpProcessor** - 命令处理器
   - 解析JSON-RPC和文本命令
   - 格式化响应消息
   - 命令类型识别

3. **McpExecutor** - 功能执行器
   - 执行具体的GUI操作
   - 参数验证和错误处理
   - 返回执行结果

4. **MainWindow** - 主界面
   - 提供GUI操作接口
   - 状态管理和显示
   - 集成MCP服务器

### 消息流程

```
客户端 → TCP连接 → McpServer → McpProcessor → McpExecutor → MainWindow → GUI操作
                    ↓
                 响应格式化 ← 执行结果 ← UI反馈
                    ↓
            客户端 ← TCP响应
```

## ⚙️ 配置选项

### 修改监听端口
在 `mainwindow.cpp` 中修改：
```cpp
// 将8088改为其他端口
if (!m_mcpServer->startServer(8088)) {
```

### 添加新命令
1. 在 `mcpprocessor.h` 中添加新的 `CommandType` 枚举
2. 在 `mcpprocessor.cpp` 中添加解析逻辑
3. 在 `mcpexecutor.h/.cpp` 中添加执行方法
4. 在 `mcpserver.cpp` 中添加命令处理

### 自定义登录验证
修改 `mainwindow.cpp` 中的 `performLogin` 方法：
```cpp
bool MainWindow::performLogin(const QString& account, const QString& password)
{
    // 在这里添加真实的登录验证逻辑
    // 例如：连接数据库、调用API等
    return authenticateUser(account, password);
}
```

## 🐛 故障排除

### 常见问题

**Q: 服务器启动失败**
A: 检查8088端口是否被占用，可以使用 `netstat -an | grep 8088` 查看

**Q: 客户端连接被拒绝**  
A: 确认防火墙设置，Windows可能需要允许程序通过防火墙

**Q: 命令执行无响应**
A: 查看应用控制台输出，检查命令格式是否正确

**Q: JSON解析失败**
A: 确保JSON格式正确，特别注意引号和逗号

**Q: MCP调用和手动点击行为是否一致**
A: 是的，现在MCP调用和手动点击按钮的行为完全一致，都会显示弹窗确认结果

### 调试模式
应用使用 `qDebug()` 输出详细日志，运行时可以看到：
- 服务器启停状态
- 客户端连接信息  
- 命令解析过程
- 执行结果反馈

## 📝 开发日志

- **v1.0.3** - 统一行为模式
  - MCP调用和手动点击行为完全一致
  - 所有操作都显示弹窗确认
  - 简化命令设计，去除复杂模式

- **v1.0.1** - 修复递归调用问题
  - 修复测试按钮无限循环点击问题
  - 端口号从8080改为8088
  - 优化代码结构，避免递归调用

- **v1.0.0** - 基础MCP功能实现
  - TCP服务器通信
  - 登录和测试按钮控制
  - JSON-RPC协议支持
  - 状态查询功能

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

## 📄 许可证

MIT License

## 📞 支持

如有问题，请通过以下方式联系：
- 创建Issue
- 发送邮件
- 项目讨论区

---
**注意**：这是一个演示项目，生产环境使用时请添加适当的安全措施和错误处理。 