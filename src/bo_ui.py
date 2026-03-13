import tkinter as tk
from PIL import Image, ImageTk
import os
import time

class BOStatusUI:
    """驳 · 极简交互载体 (Stealth Mode)"""
    def __init__(self, callback=None):
        self.root = tk.Tk()
        self.root.title("神思矩阵 · 驳 (Agent)")
        
        # 物理显影补丁：使用标准装饰窗口确保 Wayland 可见 (智力反馈版)
        self.root.geometry("800x180+400+300") 
        self.root.attributes("-topmost", True)
        self.root.configure(bg='#121212')
        self.callback = callback

        # --- Top Bar (Inputs) ---
        top_frame = tk.Frame(self.root, bg='#121212')
        top_frame.pack(side='top', fill='x', pady=5)

        # 视觉载体 (Beast Avatar) - Cross-Platform Pathing
        try:
            # 获取脚本所在目录的绝对路径，向上查找 assets
            script_dir = os.path.dirname(os.path.abspath(__file__))
            asset_path = os.path.join(os.path.dirname(script_dir), "assets", "logo_ts.webp")
            if os.path.exists(asset_path):
                pil_img = Image.open(asset_path).resize((40, 40), Image.Resampling.LANCZOS)
                self.avatar_img = ImageTk.PhotoImage(pil_img)
                tk.Label(top_frame, image=self.avatar_img, bg='#121212').pack(side='left', padx=10)
        except:
            tk.Label(top_frame, bg='#00FF00', width=4, height=2).pack(side='left', padx=10)

        # 执行反馈灯 (Pulse LED)
        self.canvas = tk.Canvas(top_frame, width=30, height=30, bg='#121212', highlightthickness=0)
        self.led = self.canvas.create_oval(5, 5, 25, 25, fill='#003300', outline='#006600')
        self.canvas.pack(side='left', padx=5)

        # 交互输入框 (Command Focus)
        self.entry = tk.Entry(top_frame, bg='#1a1a1a', fg='#00ff00', font=('Monospace', 14),
                             borderwidth=0, insertbackground='#00ff00')
        self.entry.pack(side='left', fill='x', expand=True, padx=15)
        self.entry.bind('<Return>', self.handle_return)
        
        # --- Bottom Bar (Results) ---
        result_frame = tk.Frame(self.root, bg='#121212')
        result_frame.pack(side='top', fill='both', expand=True, padx=20, pady=10)
        
        self.result_text = tk.Text(result_frame, bg='#121212', fg='#00e6e6', font=('Monospace', 11),
                                  borderwidth=0, highlightthickness=0, wrap='word', height=5)
        self.result_text.pack(side='left', fill='both', expand=True)
        
        scrollbar = tk.Scrollbar(result_frame, command=self.result_text.yview, bg='#121212')
        # scrollbar.pack(side='right', fill='y') # Optional: hide for extreme minimalism
        self.result_text.config(yscrollcommand=scrollbar.set)
        
        self.result_text.insert('1.0', "Agent Matrix Standby...")
        self.result_text.config(state='disabled')

        # 启动即夺取焦点
        self.entry.focus_force()

        self.root.attributes("-topmost", True)
        self.root.lift()

    def handle_return(self, event):
        cmd = self.entry.get().strip()
        if not cmd: return
        
        # 思考脉冲 (Thinking)
        self.set_pulse(color='#0000FF') # Blue for thinking
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', "● Reasoning...")
        self.result_text.config(state='disabled')
        
        if self.callback:
            # 延迟执行以展示思考状态
            self.root.after(100, lambda: self.callback(cmd))
        
        self.entry.delete(0, tk.END)

    def set_result(self, text):
        """显示分析结果"""
        self.result_text.config(state='normal')
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert('1.0', text)
        self.result_text.config(state='disabled')
        self.result_text.see(tk.END)
        self.set_pulse(color='#00FF00') # Green for completion

    def set_pulse(self, color='#00FF00'):
        """物理脉冲：颜色可选"""
        self.canvas.itemconfig(self.led, fill=color)
        self.root.update()
        if color != '#003300':
            self.root.after(800, lambda: self.canvas.itemconfig(self.led, fill='#003300'))

    def run(self):
        self.root.deiconify()
        self.root.lift()
        self.root.mainloop()
