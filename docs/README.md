# 📜 驳 (BO) 语音智能体

## 系统概述

驳 (BO) 是一个基于状态机驱动的语音智能体，采用玄武黑 (#0B0B0B) 审美设计，提供零界面干扰的后台常驻服务。

## 核心特性

- 🎯 **状态机架构**: IDLE → ACTIVE → EXECUTING → IDLE
- 🗣️ **语音识别**: 基于Faster-Whisper的混合模式识别
- 🧠 **智能解析**: 本地LLM命令解析，支持中英文
- ⚡ **技能矩阵**: 剪贴板、搜索、文件整理等核心技能
- 🎨 **极简设计**: 玄武黑主题，零界面干扰

## 快速开始

### 1. 安装依赖

```bash
# 安装系统依赖 (Ubuntu/Debian)
sudo apt update
sudo apt install python3-pip python3-dev portaudio19-dev

# 安装Python依赖
./start_bo.sh --install
```

### 2. 启动系统

```bash
# 语音模式 (默认)
./start_bo.sh voice

# 命令行模式
./start_bo.sh cli

# 测试模式
./start_bo.sh test

# 调试模式
./start_bo.sh debug
```

### 3. 使用方法

#### 语音模式
- 说 "驳" 唤醒系统
- 然后说出命令，如:
  - "复制这段文字"
  - "搜索Python教程"
  - "整理桌面"
  - "粘贴"

#### 命令行模式
```bash
BO> 复制测试文本
BO> 搜索天气信息
BO> 整理桌面
BO> 粘贴
```

## 技能矩阵

### ⭐ 剪贴板技能
- **复制**: 直接内存读取选中文本
- **粘贴**: 在光标位置插入剪贴板内容

### 🌐 搜索技能
- **Google搜索**: 自动打开浏览器搜索
- **查询解析**: 智能提取搜索关键词

### 🏢 文件整理技能
- **桌面整理**: 按类型自动分类文件
- **项目整理**: 工程文件结构优化
- **自动整理**: 智能文件归类

## 系统架构

```
BO Voice System
├── bo_core.py      # 核心状态机与技能管理
├── bo_voice.py     # 语音识别层 (Faster-Whisper)
├── bo_llm.py       # 命令解析器 (本地LLM)
├── bo_cli.py       # CLI接口与模式切换
├── start_bo.sh     # 启动脚本
└── requirements.txt # 依赖清单
```

### 🌐 全局 AI 技能 (Added via Antigravity)
- **bo_summary**: 物理映射剪贴板，级联生成文本摘要。
- **bo_web_search**: 自动化意图检索，支持双引擎跳转。

## 技术约束

- ✅ **禁止键盘模拟**: 使用系统API直接操作
- ✅ **低功耗设计**: IDLE状态最小化资源占用
- ✅ **本地处理**: 语音识别和命令解析本地完成
- ✅ **实时响应**: 状态机确保快速响应

## 配置说明

### 环境变量
- `BO_HOME`: 系统运行目录
- `PYTHONPATH`: Python模块路径

### 自定义配置
- 唤醒词: 默认 "驳"
- 采样率: 16kHz
- 超时时间: 5秒

## 故障排除

### 常见问题

1. **麦克风权限**
   ```bash
   # 检查麦克风设备
   arecord -l
   
   # 添加用户到audio组
   sudo usermod -a -G audio $USER
   ```

2. **依赖安装失败**
   ```bash
   # 更新pip
   pip3 install --upgrade pip
   
   # 单独安装问题包
   pip3 install pyaudio
   ```

3. **语音识别不工作**
   ```bash
   # 测试麦克风
   arecord -f cd -d 5 test.wav
   
   # 检查音频驱动
   lsmod | grep snd
   ```

### 调试模式
```bash
# 启用详细日志
./start_bo.sh debug

# 查看日志
tail -f ~/.local/share/bo/logs/bo.log
```

## 开发指南

### 添加新技能

1. 继承 `BOSkill` 基类
2. 实现 `execute()` 和 `validate()` 方法
3. 在 `BOVoiceCore._register_skills()` 中注册
4. 在 `BOLLMCommander` 中添加意图模式

### 示例技能
```python
class BOCustomSkill(BOSkill):
    def execute(self, command: BOCommand) -> Dict[str, Any]:
        # 技能执行逻辑
        return {"status": "success", "result": "..."}
    
    def validate(self, command: BOCommand) -> bool:
        # 命令验证逻辑
        return True
```

## 系统状态

- **IDLE**: 低功耗监听，等待唤醒
- **ACTIVE**: 语音识别，解析意图
- **EXECUTING**: 技能执行，返回结果
- **ERROR**: 异常处理，状态恢复

## 许可证

本项目遵循 SHENSIST_ARCH_SOUL 协议。

---

📜 **设计理念**: 绝对冷静、零界面干扰、后台常驻、随叫随到
