#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/16 09:22
# @Author  : 0x00A0
# @File    : ProgressBar.py
# @Description : TKINTER进度条窗口

from tkinter import *
from tkinter import ttk

class ProgressBar():
	def __init__(self):
		pass
	def start(self,window):
		self.top = Toplevel()
		self.master = self.top
		self.top.attributes("-toolwindow", 1)
		self.top.wm_attributes("-topmost", 1)
		# self.top.overrideredirect(True)
		self.top.title("请稍后...")
		Label(self.top, text="任务正在运行中,计算需要大量算力\n请稍等三到五分钟……\n若为第一次运行请保持网络畅通,且等待时间可能更长",font=("微软雅黑",19), fg="green").pack(pady=2)
		prog = ttk.Progressbar(self.top, mode='indeterminate', length=200)
		prog.pack(pady=10, padx=35)
		prog.start()
		self.top.resizable(False, False)
		self.top.update()
		curWidth = self.top.winfo_width()
		curHeight = self.top.winfo_height()
		scnWidth = self.top.winfo_screenwidth()
		scnHeight= self.top.winfo_screenheight()
		tmpcnf = '+%d+%d' % ((scnWidth - curWidth) / 2, (scnHeight - curHeight) / 2)
		print(scnWidth,curWidth,scnHeight,curHeight)
		self.top.geometry(tmpcnf)
		self.top.mainloop()

	def quit(self):
		if self.master:
			self.master.destroy()
