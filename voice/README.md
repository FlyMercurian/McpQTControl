# 🎤 QT应用语音控制系统

## 📋 概述

这是一个完整的语音控制系统，专门为QT应用设计，通过语音指令控制QT应用程序的各种操作。系统集成了语音录制、语音识别、自然语言处理和MCP（Model Context Protocol）客户端，实现了从语音输入到QT应用操作的完整流程。

### 🌟 核心特性

- **🎙️ 实时语音录制**：支持按键控制的语音录制，实时反馈录制状态
- **🧠 智能语音识别**：基于阿里云DashScope API，支持中文语音识别
- **💬 自然语言处理**：智能理解口语化指令，转换为结构化操作
- **🔧 MCP协议集成**：通过MCP协议与QT应用通信
- **🔄 混合输入模式**：语音+文字双重输入，互为备用
- **⚡ 异步处理**：高效的异步处理架构

## 🏗️ 技术架构

### 整体架构图

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   用户语音输入    │───▶│   语音录制模块    │───▶│   语音识别模块    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │                         │
                              ▼                         ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   音频文件存储    │    │   键盘输入监听    │    │  阿里云API调用   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                      │
                                                      ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    QT应用操作    │◀───│   MCP客户端      │◀───│  自然语言处理     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 🔗 数据流向

```
语音输入 → 音频录制 → 文件保存 → 语音识别 → 文本提取 → 指令解析 → MCP调用 → QT操作
    ↑                                                              ↓
    └──────────────────── 文字输入备用 ←─────────────────── 结果反馈
```

## 📁 模块结构

```
voice/
├── 🎯 核心模块
│   ├── main_voice.py           # 主程序入口
│   ├── voice_chat_session.py   # 语音会话管理
│   ├── voice_input.py          # 语音录制控制
│   └── speech_recognizer.py    # 语音识别引擎
├── 🔧 API模块
│   └── voice2text.py           # 阿里云API封装
├── ⚙️ 配置文件
│   ├── config.env              # 环境配置
│   └── requirements.txt        # 依赖管理
├── 🧪 测试模块
│   ├── test_voice_system.py    # 系统测试
│   ├── test_voice_api.py       # API测试
│   └── test_voice.py           # 基础测试
├── 📚 文档
│   ├── README.md               # 本文档
│   └── __init__.py             # 包定义
└── 📂 临时目录
    └── temp_audio/             # 音频文件缓存
```

## 🚀 快速开始

### 1. 环境准备

```bash
# 切换到语音模块目录
cd voice/

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置设置

编辑 `config.env` 文件：

```env
# 必须设置：阿里云DashScope API密钥
DASHSCOPE_API_KEY=sk-your-real-api-key-here

# 可选配置
VOICE_ENABLED=true                    # 启用语音功能
VOICE_MODEL=qwen-omni-turbo-0119      # 语音识别模型
MCP_SERVER_URL=http://localhost:8000  # MCP服务器地址
```

### 3. 启动系统

```bash
# 启动语音控制系统
python main_voice.py

# 或者使用命令行参数
python main_voice.py --voice-only     # 强制语音模式
python main_voice.py --text-only      # 强制文字模式
python main_voice.py --interactive    # 交互选择模式
```

## 🎤 使用方法

### 语音录制操作

| 操作 | 按键 | 说明 |
|------|------|------|
| **开始录音** | `V键` | 按下V键开始录制 |
| **结束录音** | `V键` | 再次按下V键结束录制 |
| **取消录音** | `ESC` | 取消当前录制 |
| **跳过语音** | `回车` | 跳过语音，使用文字输入 |

### 语音指令示例

```
🎙️ 语音输入示例：

用户说话："登录账号admin密码123456"
↓ 系统识别
识别结果："登录账号admin密码123456"
↓ 指令解析
JSON格式：{"tool":"login","arguments":{"account":"admin","password":"123456"}}
↓ MCP调用
QT应用执行登录操作
↓ 结果反馈
助手："登录成功！用户admin已成功登录系统。"
```

### 支持的语音指令

| 语音输入 | 功能说明 | 生成指令 |
|----------|----------|----------|
| "登录账号admin密码123" | 用户登录 | `{"tool":"login","arguments":{"account":"admin","password":"123"}}` |
| "点击测试按钮" | 按钮操作 | `{"tool":"test_button","arguments":{"random_string":"test"}}` |
| "查看应用状态" | 状态查询 | `{"tool":"get_state","arguments":{}}` |
| "退出应用" | 程序退出 | 直接退出程序 |

## 🔧 技术实现

### 1. 语音录制模块 (`voice_input.py`)

#### VoiceRecorder 类
```python
class VoiceRecorder:
    """核心录音引擎"""
    def __init__(self, sample_rate=16000, channels=1, max_duration=30):
        # 16kHz单声道，最大30秒录制
        
    def start_recording(self) -> bool:
        # 启动录音流，使用sounddevice库
        
    def stop_recording(self) -> float:
        # 停止录音并返回时长
        
    def save_recording(self, filename=None) -> str:
        # 保存为WAV格式，返回文件路径
```

#### KeyboardVoiceInput 类
```python
class KeyboardVoiceInput:
    """键盘控制接口"""
    def wait_for_voice_input(self, prompt) -> Optional[str]:
        # Windows平台：使用msvcrt监听按键
        # Unix平台：暂不支持按键录音
        
    def _windows_voice_input(self) -> Optional[str]:
        # V键切换录音状态
        # ESC取消，回车跳过
        # 实时显示录音进度
```

**设计亮点**：
- **状态机设计**：录音状态严格控制，避免重复录制
- **实时反馈**：录音进度条实时更新
- **异常处理**：音频设备异常自动恢复
- **跨平台考虑**：Windows/Unix不同实现

### 2. 语音识别模块 (`speech_recognizer.py`)

#### SpeechRecognizer 类
```python
class SpeechRecognizer:
    """语音识别核心引擎"""
    def __init__(self, model_name="qwen-omni-turbo-0119"):
        self.client = create_voice_client()  # 阿里云客户端
        
    def recognize_from_file(self, audio_file_path, custom_prompt=None) -> str:
        # 调用阿里云API进行语音识别
        # 支持自定义提示词优化识别效果
        
    def _clean_recognition_result(self, text) -> str:
        # 清理识别结果，去除API返回的多余信息
        
    def is_silent_audio(self, audio_file_path) -> bool:
        # 静音检测，避免无效API调用
```

#### VoiceCommandProcessor 类
```python
class VoiceCommandProcessor:
    """语音指令优化处理器"""
    def __init__(self, recognizer):
        self.qt_prompts = {
            'login': "将音频转为简短文字，只要指令内容：如'登录账号xxx密码xxx'",
            'button': "将音频转为简短文字，只要指令内容：如'点击测试按钮'",
            'general': "将音频转为简短文字指令，不要解释代码，只要用户说的话"
        }
        
    def process_voice_command(self, audio_file_path, command_type='general') -> str:
        # 根据指令类型使用不同的识别提示词
```

**设计亮点**：
- **提示词优化**：针对不同场景优化识别准确率
- **结果清理**：智能过滤API返回的冗余信息
- **静音检测**：文件大小预检，避免浪费API调用
- **错误恢复**：API调用失败时的降级处理

### 3. 语音会话模块 (`voice_chat_session.py`)

#### VoiceChatSession 类
```python
class VoiceChatSession(ChatSession):
    """语音聊天会话管理器"""
    def __init__(self, llm_client, mcp_client, voice_enabled=True):
        super().__init__(llm_client, mcp_client)
        self._initialize_voice_components()  # 初始化语音组件
        
    def _get_user_input(self, prompt="用户") -> str:
        # 语音优先，文字备用的混合输入模式
        
    def _process_voice_input(self, audio_file_path) -> str:
        # 语音识别 → 结果确认 → 返回文字
        
    def _confirm_voice_input(self, recognized_text, audio_file_path) -> str:
        # 用户确认：y确认/n手动输入/r重录/s跳过
```

**设计亮点**：
- **继承架构**：继承ChatSession，复用MCP客户端逻辑
- **混合输入**：语音和文字无缝切换
- **确认机制**：用户可确认、修正或重录
- **降级处理**：语音失败时自动切换到文字模式

### 4. 主程序模块 (`main_voice.py`)

#### 启动流程
```python
async def main():
    """主程序启动流程"""
    # 1. 加载配置文件
    load_env_config()
    
    # 2. 检查语音功能状态
    voice_fully_available = print_voice_status()
    
    # 3. 初始化MCP和LLM客户端
    mcp_client = MCPClient()
    llm_client = LLMClient(...)
    
    # 4. 创建语音会话
    voice_chat_session = VoiceChatSession(...)
    
    # 5. 连接MCP服务器并获取工具列表
    await mcp_client.connect_to_server(mcp_server_url)
    tools = await mcp_client.list_tools()
    
    # 6. 构建针对语音优化的系统提示词
    system_message = construct_voice_optimized_prompt(tools)
    
    # 7. 启动语音聊天会话
    await voice_chat_session.start(system_message)
```

**设计亮点**：
- **依赖检查**：启动时全面检查音频、API等依赖
- **配置管理**：优先使用voice目录配置，兼容MCP客户端配置
- **错误诊断**：详细的错误提示和解决建议
- **资源管理**：异步资源清理和异常处理

## 💡 设计理念

### 1. 用户体验优先

- **即时反馈**：录音状态、识别进度、操作结果的实时反馈
- **容错处理**：语音识别失败时的多种恢复方案
- **操作简单**：V键一键录音，直观的操作提示
- **混合模式**：语音和文字可随时切换，降低使用门槛

### 2. 技术架构稳健

- **模块解耦**：每个模块职责单一，便于测试和维护
- **异步设计**：全程异步处理，避免UI卡顿
- **异常隔离**：单个模块异常不影响整体系统
- **资源管理**：严格的资源生命周期管理

### 3. 性能优化考虑

- **智能静音检测**：避免无效的API调用
- **音频格式优化**：16kHz单声道，平衡质量与效率
- **临时文件管理**：录音后自动清理，避免磁盘占用
- **API调用优化**：批量处理、错误重试机制

### 4. 扩展性设计

- **提示词可配置**：不同场景使用不同的识别提示词
- **多API支持**：支持多种LLM和语音识别提供商
- **插件化架构**：新的语音指令类型易于添加
- **配置驱动**：核心参数通过配置文件控制

## 🔍 核心算法

### 语音指令解析流程

```python
def voice_command_pipeline(audio_file):
    """语音指令处理管道"""
    
    # 1. 预检查：文件大小和格式验证
    if not validate_audio_file(audio_file):
        return None
        
    # 2. 静音检测：避免无效API调用
    if is_silent_audio(audio_file):
        return ""
        
    # 3. 语音识别：调用阿里云API
    raw_result = call_dashscope_api(audio_file, prompt)
    
    # 4. 结果清理：去除API返回的冗余信息
    cleaned_text = clean_recognition_result(raw_result)
    
    # 5. 指令标准化：将自然语言转换为标准格式
    if is_login_command(cleaned_text):
        return standardize_login_command(cleaned_text)
    elif is_button_command(cleaned_text):
        return standardize_button_command(cleaned_text)
    else:
        return cleaned_text
```

### LLM指令生成优化

```python
def construct_voice_optimized_prompt(tools):
    """构建语音优化的系统提示词"""
    return f"""
    你是QT应用语音控制助手，专门处理口语化指令。
    
    语音识别容错规则：
    1. "登陆"→"登录"，"测试下按钮"→"点击测试按钮"
    2. 从"用户名wyx密码123"中提取结构化参数
    3. 支持不完整指令，主动询问缺失信息
    
    响应格式：严格JSON，无Markdown，无解释前缀
    {{
        "tool": "tool-name",
        "arguments": {{"param": "value"}}
    }}
    
    可用工具：{json.dumps(tools, ensure_ascii=False)}
    """
```

## 🧪 测试指南

### 完整系统测试

```bash
# 运行完整测试套件
python test_voice_system.py

# 测试输出示例：
# 🎤 语音控制系统完整测试
# ✓ 环境配置: 通过
# ✓ 依赖检查: 通过  
# ✓ 音频系统: 通过
# ✓ 语音模块: 通过
# ✓ MCP连接: 通过
# ✓ 系统集成: 通过
# ✓ 语音识别: 通过
# 🎉 所有测试通过！
```

### 单模块测试

```bash
# 测试语音录制
python voice_input.py

# 测试语音识别
python speech_recognizer.py

# 测试语音会话
python voice_chat_session.py

# 测试API调用
python test_voice_api.py
```

## 🐛 故障排除

### 常见问题诊断

| 问题症状 | 可能原因 | 解决方案 |
|----------|----------|----------|
| **401 API错误** | API密钥无效 | 检查config.env中的DASHSCOPE_API_KEY |
| **录音设备错误** | 麦克风权限/驱动 | 检查系统麦克风设置和权限 |
| **导入模块失败** | 依赖缺失 | 运行 `pip install -r requirements.txt` |
| **MCP连接失败** | 服务器未启动 | 确保MCP服务器在运行 |
| **识别结果为空** | 录音质量差/静音 | 检查麦克风音量，重新录制 |

### 详细调试方法

```bash
# 开启详细日志
export LOG_LEVEL=DEBUG

# 或在config.env中设置
ENABLE_DEBUG_LOG=true
LOG_LEVEL=DEBUG

# 运行时会显示详细的调试信息
INFO:voice_input:开始录音...
INFO:speech_recognizer:开始识别音频文件: voice_record_xxx.wav
INFO:speech_recognizer:语音识别完成: 登录账号admin密码123
INFO:voice_chat_session:解析指令: {"tool":"login",...}
```

## 📈 性能监控

### 关键性能指标

- **录音延迟**: < 100ms（录音启动时间）
- **识别速度**: 2-5秒（取决于音频长度和网络）
- **内存占用**: < 50MB（不包含临时音频文件）
- **API调用**: 每次识别1次调用（优化后避免重复调用）

### 优化建议

```python
# 音频参数优化
VOICE_SAMPLE_RATE=16000    # 16kHz足够语音识别
MAX_RECORDING_DURATION=10  # 限制录音时长减少处理时间

# API调用优化
AUTO_CONFIRM_VOICE=true    # 自动确认减少交互
VOICE_ENABLED=false        # 在测试环境可临时禁用
```

## 🔮 未来扩展

### 计划功能

- **🌐 多语言支持**：英文、日语等语音识别
- **🎯 场景优化**：针对不同应用场景的专用提示词
- **📱 移动端适配**：Android/iOS语音输入支持
- **🔊 语音合成**：TTS反馈，完整的语音交互闭环
- **🧠 本地识别**：集成离线语音识别，降低API依赖

### 扩展接口

```python
# 自定义语音指令处理器
class CustomCommandProcessor(VoiceCommandProcessor):
    def process_custom_command(self, audio_file, context):
        # 实现自定义处理逻辑
        pass

# 多语言识别支持
class MultiLanguageRecognizer(SpeechRecognizer):
    def __init__(self, languages=['zh', 'en']):
        # 支持多语言识别
        pass
```

## 📞 支持与联系

- **问题反馈**：请提交Issue描述具体问题
- **功能建议**：欢迎提交Feature Request
- **技术讨论**：参与项目Discussion
- **文档改进**：欢迎提交文档优化PR

---

**🎯 核心理念**：让语音控制变得简单、可靠、高效！

通过精心设计的架构和用户体验，实现从语音输入到QT应用操作的无缝衔接，为用户提供自然、直观的人机交互体验。 