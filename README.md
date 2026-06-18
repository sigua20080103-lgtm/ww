# 📅 智能 Apple 日历助手 (Smart Apple Calendar AI)

这是一个基于 Python 编写的 macOS 桌面级提效小工具。它利用 **DeepSeek AI** 的自然语言处理能力，让你只需输入一句“大白话”（例如：“下周三下午两点半去图书馆复习”），就能自动解析出标准时间，并秒级录入到 **Apple Calendar (苹果自带日历)** 中。

## ✨ 核心特性

* **🤖 自然语言智能解析**：不需要繁琐地手动选择年月日时分，直接输入模糊或相对时间表达（如“明天早晨”、“下周五下午”），AI 自动帮你算准时间。
* **💻 极简原生 GUI**：使用 Tkinter 构建的极简弹窗，轻量且反应迅速。
* **⚡️ 流畅多线程处理**：网络请求采用独立线程，UI 界面绝不卡顿、假死。
* **🛡️ 安全沙盒确认机制**：AI 提取完成后会先唤起 macOS 原生日历的确认弹窗，由你做最后一步人工核对，安全且万无一失。

## 🛠️ 环境准备与依赖

本工具专为 **macOS** 系统设计。在使用前，请确保您的电脑已安装 Python 3。

**1. 安装 Python 依赖库：**
在终端 (Terminal) 中运行以下命令安装必要的包：
```bash
pip3 install requests icalendar

(注：如果使用的是较新的 macOS 且提示被系统拦截，可以尝试使用虚拟环境，或在命令后加上 --break-system-packages)
2. 安装 Tkinter 图形库（如 macOS 默认缺失）：
brew install python-tk

⚙️ 配置与使用
安全提示：本仓库的代码已抹除真实的 API Key，使用前请先配置您自己的 Key！
	1.	前往 DeepSeek 开放平台 注册并获取您的 API Key。
	2.	用文本编辑器打开 calendar_app.py，找到文件开头的 配置区：
# ================= 配置区 =================
API_KEY = "替换为您的真实_DEEPSEEK_API_KEY"
API_URL = "[https://api.deepseek.com/chat/completions](https://api.deepseek.com/chat/completions)"
MODEL_NAME = "deepseek-v4-pro"
# ==========================================

	3.	保存后，在终端运行该脚本即可弹出智能助手窗口：
python3 calendar_app.py

📦 进阶：打包为独立的 Mac App
如果您不想每次都通过终端运行，可以使用 PyInstaller 将其打包成一个标准的桌面 .app 软件（可直接固定到程序坞）：
	1.	安装打包工具：
pip3 install pyinstaller

	2.	在脚本所在目录执行打包命令：
python3 -m PyInstaller --noconsole --windowed calendar_app.py

	3.	打包完成后，在生成的 dist/ 文件夹下即可找到 calendar_app.app 应用程序。双击即可使用！
本项目基于 MIT License 开源，欢迎 Fork、提交 PR 共同优化这个提效小工具！
