#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/13 15:04
# @Author  : 0x00A0
# @File    : main.py
# @Description : TKINTER窗口程序

import asyncio
import multiprocessing
import os
import re
import shutil
import sys
import threading
import time
import tkinter
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar

import paddle
import predict
from ProgressBar import ProgressBar
from ppgan.apps import StyleGANv2EditingPredictor
from ppgan.apps import Pixel2Style2PixelPredictor
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk

shutil.rmtree("img")
os.mkdir("img")
"""
=================================================
主窗口
=================================================
"""
root = Tk()
root.title("人脸时光机")
# root.resizable(False,False)  # 不可缩放
root.minsize(1000, 750)
h_box = w_box = root.winfo_screenwidth() / 4  # 指定图片框的最大大小为屏幕的1/4
window = tk.Frame(root)
prog = None
global photo0
global photo1
global done
done = False

"""
=================================================
控件定义
=================================================
"""
work_path = os.getcwd()
ori_path = ""  # 图片路径


#   ===原始图片框===
def resize(w, h, w_box, h_box, pil_image):
	"""
	对一个pil_image对象进行缩放，让它在一个矩形框内，还能保持比例
	"""
	f1 = 1.0 * w_box / w
	f2 = 1.0 * h_box / h
	factor = min([f1, f2])
	width = int(w * factor)
	height = int(h * factor)
	return pil_image.resize((width, height), Image.ANTIALIAS)


img0 = Image.open(os.path.join("statics", "L.png"))
w, h = img0.size
img0 = resize(w, h, w_box, h_box, img0)
photo0 = ImageTk.PhotoImage(img0)
imgbox_ori = Label(window, image=photo0)
lbl_ori = Label(window, text="原始图像", font=("微软雅黑", 19))

#   ===生成图片框===
img1 = Image.open(os.path.join("statics", "R.png"))
w, h = img1.size
img1 = resize(w, h, w_box, h_box, img1)
photo1 = ImageTk.PhotoImage(img1)
imgbox_dst = Label(window, image=photo1)
lbl_dst = Label(window, text="生成图像", font=("微软雅黑", 19))


#   ===打开图片按钮===
def openImg():
	filename = filedialog.askopenfilename()
	if filename != '':
		global ori_path
		ori_path = filename
		img0 = Image.open(ori_path)
		w, h = img0.size
		img0 = resize(w, h, w_box, h_box, img0)
		global photo0
		photo0 = ImageTk.PhotoImage(img0)
		imgbox_ori.configure(image=photo0)
		img1 = Image.open(os.path.join("statics", "R.png"))
		w, h = img1.size
		img1 = resize(w, h, w_box, h_box, img1)
		global photo1
		photo1 = ImageTk.PhotoImage(img1)
		imgbox_dst.configure(image=photo1)
	else:
		messagebox.showinfo("提示", "您没有选择任何文件")


func_openImg = window.register(openImg)  # 必要的函数包装
btn_OpenImg = Button(window, text="打开图片", font=("微软雅黑", 19), command=func_openImg)

#   ===年龄输入框===
lbl_Age = Label(window, text="需要增长的年龄(负数表示年轻):", font=("微软雅黑", 19))


def checkInput(content):
	"""
	只允许输入框输入数字和正负号
	"""
	if re.match(r"^-?(\.\d+|\d+(\.\d+)?)", content) or content == '-' or content == "":
		return True
	else:
		return False


val_var = tk.StringVar(value="0")
func_checkInput = window.register(checkInput)  # 必要的函数包装
txt_Age = Entry(window, font=("微软雅黑", 19), textvariable=val_var, validate="key",
                validatecommand=(func_checkInput, '%P'))


#   ===图片生成按钮===

def getDistance(age):
	if age > 0:
		return age / 10
	else:
		return age / 15


def getResult():
	global done
	if done:
		if os.path.exists(os.path.join(work_path, "img", "dst.editing.png")):
			img1 = Image.open(os.path.join(work_path, "img", "dst.editing.png"))
			w, h = img1.size
			img1 = resize(w, h, w_box, h_box, img1)
			global photo1
			photo1 = ImageTk.PhotoImage(img1)
			imgbox_dst.configure(image=photo1)
			prog.quit()
			btn_genImg["state"] = "normal"
			messagebox.showinfo("提示", "图片生成完成", parent=root)
			shutil.copy(os.path.join(work_path, "img", "dst.editing.png"),
			            ''.join(os.path.normpath(ori_path).split(r"\\")[:-1]))
			done = False
			return
	root.after(1000, getResult)


def pred():
	try:
		predictor = predict.predictor(os.path.normpath(ori_path), os.path.join(work_path, "img"),
		                              getDistance(int(txt_Age.get())))
		predictor.predict()
	except Exception as e:
		prog.quit()
		btn_genImg["state"] = "normal"
		messagebox.showerror("错误", ''.join(e.args), parent=root)
	global done
	done = True


def genImg():
	shutil.rmtree("img")
	os.mkdir("img")
	btn_genImg["state"] = "disabled"
	if txt_Age.get() == "" or txt_Age.get() == "-":
		messagebox.showinfo("提示", "未填写年龄", parent=root)
	print((os.path.normpath(ori_path), os.path.join(work_path, "img"), getDistance(int(txt_Age.get()))))
	th = threading.Thread(target=pred)
	th.setDaemon(True)  # 标记成Daemon以防止出现孤儿进程
	th.start()
	root.after(1000, getResult)
	global prog
	prog = ProgressBar()
	prog.start(root)


func_genImg = window.register(genImg)  # 必要的函数包装
btn_genImg = Button(window, text="生成照片", font=("微软雅黑", 19), command=func_genImg)

#   ===About信息===
lbl_about = Label(window, text="技术支持: 百度Paddle提供深度学习框架与模型\n" +
                               "   开源地址: https://github.com/PaddlePaddle/Paddle\n" +
                               "本项目已开源至GitHub\n" +
                               "   开源地址: https://github.com/0x00A0/FaceAge",
                  font=("微软雅黑", 9),
                  foreground="#45AA48"
                  )

"""
=================================================
放置所有控件
=================================================
"""
window.place(anchor="center", relx=.50, rely=.50)
lbl_ori.grid(row=0, column=0, rowspan=1, columnspan=4)
imgbox_ori.grid(row=1, column=0, rowspan=4, columnspan=4, sticky="NSWE")
lbl_dst.grid(row=0, column=5, rowspan=1, columnspan=4)
imgbox_dst.grid(row=1, column=5, rowspan=4, columnspan=4, sticky="NSWE")
btn_OpenImg.grid(row=6, column=0, rowspan=1, columnspan=10, sticky="WE")
lbl_Age.grid(row=7, column=0, rowspan=1, columnspan=4, sticky="WE")
txt_Age.grid(row=7, column=5, rowspan=1, columnspan=4, sticky="WE")
btn_genImg.grid(row=8, column=0, rowspan=1, columnspan=10, sticky="WE")
lbl_about.grid(row=9, column=0, rowspan=1, columnspan=10, sticky="WE")

"""
=================================================
调用mainloop()显示主窗口
=================================================
"""
window.mainloop()
