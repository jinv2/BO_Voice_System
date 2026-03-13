# 神思矩阵 · 驳 (BO) 安装与部署教程 (全平台)

本文档旨在引导您在 Windows、macOS 及 Linux 系统上顺利部署 **“驳” (BO)** 智能体。请严格按照所属系统的步骤执行。

---

## 1. 基础环境校验
“驳” 运行于 Python 环境。请确保您的系统已安装：
- **Python 3.10+** (推荐版本)
- **pip** (Python 包管理器)
- **Ollama (Qwen2)** (可选：仅在需要极高复杂的自然语言理解时使用，基础版内置的原生逻辑引擎已足够处理所有日常商务指令)

验证指令：
```bash
python --version
pip --version
```

---

## 2. 核心依赖安装
在所有平台上，请先运行以下指令安装基础图形与 GUI 库：
```bash
pip install pillow pyperclip
```

---

## 3. 操作系统特定配置 (关键)

### 🪟 Windows 部署指南
1.  **首选终端**：强烈建议安装 **Windows Terminal**。
2.  **设置执行策略**：以管理员身份打开 PowerShell，执行以下命令以允许脚本运行：
    ```powershell
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    ```
3.  **显示设置**：
    - 建议缩放比例为 **100%**。
    - 物理控制技能（如 F2 重命名）需要系统焦点在目标窗口。

### 🍎 macOS 部署指南
1.  **辅助功能权限**：
    - 进入 `系统设置` -> `隐私与安全性` -> `辅助功能`。
    - 将 `终端 (Terminal)` 或您使用的 IDE (如 VS Code) 添加到允许列表并勾选。
    - *原因*：Agent 需要此权限来模拟键盘按键。
2.  **多媒体增强**：
    - 安装 [Homebrew](https://brew.sh/)：`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
    - 运行：`brew install ffmpeg` (用于视频处理与音频分析)。

### 🐧 Linux (Ubuntu/Debian) 部署指南
1.  **系统级依赖**：
    ```bash
    sudo apt update
    sudo apt install python3-tk xdotool xclip ffmpeg
    ```
2.  **Wayland 用户注意**：
    - “驳” 的交互条 (Zenith Bar) 基于 Tkinter，部分 Wayland 环境下置顶功能可能受限，建议在 X11 会话下运行。

---

## 4. 启动 “驳”
进入项目根目录的 `src` 文件夹：
```bash
python bo_cli.py
```
或启动图形化界面：
```bash
python bo_ui.py
```

---

## 5. 生成可执行文件 (简单交付模式)
如果您需要将“驳”打包并交给其他没有 Python 环境的客户，请在根目录下运行：
```bash
python build_cross_platform.py
```
该脚本会自动为您生成当前系统的独立文件夹 `BO_Matrix_Dist`。
- **注意**：由于操作系统的差异，您必须在 **Windows** 上运行此脚本生成 Windows 版，在 **Mac** 上运行生成 Mac 版。

---

## 🛠️ 故障排查 (Troubleshooting)
- **Permission Denied**：在 Linux/Mac 上，确保您对目录有写入权限，或尝试用非 root 用户运行。
- **Tkinter Missing**：如果提示 `ImportError: No module named '_tkinter'`，请参考第3部分的系统依赖安装命令。
- **控制失效**：检查第3部分的“辅助功能”权限或 PowerShell 执行策略。

---
**技术支持**：如遇疑难杂症，可直接在交互窗口询问 Agent，它将为您提供环境自检指令。
