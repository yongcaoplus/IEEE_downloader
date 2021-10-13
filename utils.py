# -*- coding: utf-8 -*-
# @Time    : 2021/10/13 12:16 
# @Author  : Yong Cao
# @Email   : yongcao_epic@hust.edu.cn
import os
import requests
from tkinter import *
from tkinter.ttk import *
import time


def get_window_size(win, update=True):
    """ 获得窗体的尺寸 """
    if update:
        win.update()
    return win.winfo_width(), win.winfo_height(), win.winfo_x(), win.winfo_y()


def center_window(win, width=None, height=None):
    """ 将窗口屏幕居中 """
    screenwidth = win.winfo_screenwidth()
    screenheight = win.winfo_screenheight()
    if width is None:
        width, height = get_window_size(win)[:2]
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 3)
    win.geometry(size)



def downLoad_paper(paper_info, show_bar=False):
    print("\n" * 2)
    print(show_bar)
    print("执行开始".center(len(paper_info) + 28, '-'))
    succeed = True
    paper_downloaded = 0
    already_exist = 0
    if show_bar:
        root = Tk()
        root.geometry("300x140+600+300")
        root.iconbitmap("img/root.ico")  # 窗体图标
        root.title("下载进度")
        center_window(root)
        pb = Progressbar(root, length=200, mode="determinate", orient=HORIZONTAL)
        pb.pack(padx=10, pady=20)
        pb["value"] = 0
        pb["maximum"] = len(paper_info)
    start = time.perf_counter()
    for i, item in enumerate(paper_info.keys()):
        if show_bar:
            pb["value"] = i
            root.update()
        papername = paper_info[item]['name']
        paperurl = paper_info[item]['url']
        # 文件存储
        if os.path.exists(papername):
            already_exist += 1
            continue
        try:
            r = requests.get(paperurl)
            with open(papername, 'wb+') as f:
                f.write(r.content)
                paper_downloaded += 1
            # 停一下防禁ip
            time.sleep(1)
        except Exception as e:
            print(e)
            print("unknown name! parser error", papername)
            succeed = False
        a = '*' * i
        b = '.' * (len(paper_info) - i)
        c = (i / len(paper_info)) * 100
        t = time.perf_counter() - start
        print("\r任务进度:{:>3.0f}% [{}->{}]消耗时间:{:.2f}s".format(c, a, b, t), end="")
    if show_bar:
        del root
    print("\n"+"执行结束".center(len(paper_info)+28,'-'))
    print("-"*50)
    print("Downloaded {} papers and {} paper already exists.".format(paper_downloaded, already_exist))
    print("-" * 50)
    return succeed, paper_downloaded, already_exist