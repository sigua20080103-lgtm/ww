import tkinter as tk
from tkinter import messagebox
import threading
import json
import requests
import subprocess
from datetime import datetime
from icalendar import Calendar, Event

# ================= 配置区 =================
# ⚠️ 警告：上传到 GitHub 时请勿填写真实的 Key，以防泄露！
# 请在此处填入您从 DeepSeek 开放平台申请的 API Key
API_KEY = "YOUR_DEEPSEEK_API_KEY_HERE"
API_URL = "https://api.deepseek.com/chat/completions" # 以 DeepSeek 为例
MODEL_NAME = "deepseek-v4-pro"
# ==========================================

def parse_text_to_json(text):
    """调用 API 将自然语言转换为结构化的 JSON 日期数据"""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prompt = f"""
    你是一个日程解析助手。当前时间是：{current_time}。
    请从以下用户的输入中提取日程信息，并严格以 JSON 格式输出，不要包含任何 markdown 标记。
    如果没有明确给出结束时间，默认设定为开始时间的一小时后。
    
    必须输出的 JSON 格式：
    {{
        "title": "事件标题",
        "start": "YYYY-MM-DD HH:MM:SS",
        "end": "YYYY-MM-DD HH:MM:SS"
    }}
    用户输入："{text}"
    """
    
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": MODEL_NAME, "messages": [{"role": "user", "content": prompt}], "temperature": 0.1}

    response = requests.post(API_URL, headers=headers, json=payload, timeout=15)
    response.raise_for_status()
    
    result_text = response.json()['choices'][0]['message']['content'].strip()
    # 兼容可能带有 markdown 块的返回
    if result_text.startswith("```json"):
        result_text = result_text[7:-3].strip()
    elif result_text.startswith("```"):
        result_text = result_text[3:-3].strip()
        
    return json.loads(result_text)

def create_and_open_ics(event_data):
    """生成 .ics 并用 Apple Calendar 打开"""
    cal = Calendar()
    cal.add('prodid', '-//Smart Apple Calendar AI Assistant//')
    cal.add('version', '2.0')
    
    event = Event()
    event.add('summary', event_data['title'])
    event.add('dtstart', datetime.strptime(event_data['start'], "%Y-%m-%d %H:%M:%S"))
    event.add('dtend', datetime.strptime(event_data['end'], "%Y-%m-%d %H:%M:%S"))
    cal.add_component(event)

    temp_file = "/tmp/temp_event.ics"
    with open(temp_file, 'wb') as f:
        f.write(cal.to_ical())
        
    # 唤起 macOS 原生日历应用
    subprocess.run(["open", temp_file])

# ================= 前端 UI 逻辑 =================

def on_submit():
    user_input = entry.get()
    if not user_input.strip():
        messagebox.showwarning("提示", "请输入日程信息！")
        return
        
    # 禁用按钮，展示加载状态
    btn.config(state=tk.DISABLED, text="AI 思考中...")
    
    # 异步线程处理网络请求，防止 Tkinter 界面假死
    def worker():
        try:
            parsed_data = parse_text_to_json(user_input)
            create_and_open_ics(parsed_data)
            # 成功后清空输入框
            root.after(0, lambda: entry.delete(0, tk.END))
        except Exception as e:
            root.after(0, lambda: messagebox.showerror("错误", f"解析失败：\n{str(e)}"))
        finally:
            # 恢复按钮状态
            root.after(0, lambda: btn.config(state=tk.NORMAL, text="生成并加入日历"))
            
    threading.Thread(target=worker, daemon=True).start()

if __name__ == "__main__":
    # 构建主窗口
    root = tk.Tk()
    root.title("智能日程助手")
    root.geometry("400x150")
    root.eval('tk::PlaceWindow . center')  # 窗口居中

    # 界面元素
    label = tk.Label(root, text="输入日程安排 (例如: 下周二下午3点去健身)", font=("Arial", 13))
    label.pack(pady=10)

    entry = tk.Entry(root, font=("Arial", 14), width=32)
    entry.pack(pady=5)
    entry.bind('<Return>', lambda event: on_submit())  # 支持回车键直接提交

    btn = tk.Button(root, text="生成并加入日历", font=("Arial", 13), command=on_submit)
    btn.pack(pady=10)

    root.mainloop()
