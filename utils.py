# -*- coding: utf-8 -*-
# @Time    : 2021/10/13 12:16 
# @Author  : Yong Cao
# @Email   : yongcao_epic@hust.edu.cn
import os
import requests
import time


def _init():
    # 初始化一个全局的字典
    global _global_dict
    _global_dict = {}


def set_value(key, value):
    _global_dict[key] = value


def get_value(key):
    try:
        return _global_dict[key]
    except KeyError as e:
        print(e)



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
    print("执行开始".center(len(paper_info) + 28, '-'))
    succeed = True
    paper_downloaded = 0
    already_exist = 0
    start = time.perf_counter()
    for i, item in enumerate(paper_info.keys()):
        set_value("progress_bar_num", i)
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
    set_value("progress_bar_num", len(paper_info))
    # if show_bar:
    #     del root
    print("\n"+"执行结束".center(len(paper_info)+28,'-'))
    print("-"*50)
    print("Downloaded {} papers and {} paper already exists.".format(paper_downloaded, already_exist))
    print("-" * 50)
    return succeed, paper_downloaded, already_exist