# coding:utf-8
import _thread
import os
import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox, ttk

from PIL import Image, ImageTk

import utils
from download_paper_by_URLfile import organize_info_by_txt
from download_paper_by_pageURL import organize_info_by_query
from utils import downLoad_paper, center_window


def show_confirm(message=""):
    """
        True  : yes
        False : no
    """
    return messagebox.askyesno("确认框", message)


def error_inform(message=""):
    """
        True  : yes
        False : no
    """
    return messagebox.showerror("参数错误", message)


def show_succeed_window(message=""):
    """
        True  : yes
        False : no
    """
    return messagebox.showinfo("下载成功！", message)


def show_fail_window(message=""):
    """
        True  : yes
        False : no
    """
    return messagebox.showerror("下载失败...", message)


def show_begin_download(message=""):
    """
        True  : yes
        False : no
    """
    return messagebox.askyesno("确认框", message)


def tkimg_resized(img, w_box, h_box, keep_ratio=True):
    """对图片进行按比例缩放处理"""
    w, h = img.size

    if keep_ratio:
        if w > h:
            width = w_box
            height = int(h_box * (1.0 * h / w))

        if h >= w:
            height = h_box
            width = int(w_box * (1.0 * w / h))
    else:
        width = w_box
        height = h_box

    img1 = img.resize((width, height), Image.ANTIALIAS)
    tkimg = ImageTk.PhotoImage(img1)
    return tkimg


def image_label(frame, img, width, height, keep_ratio=True):
    """输入图片信息，及尺寸，返回界面组件"""
    if isinstance(img, str):
        _img = Image.open(img)
    else:
        _img = img
    lbl_image = tk.Label(frame, width=width, height=height)

    tk_img = tkimg_resized(_img, width, height, keep_ratio)
    lbl_image.image = tk_img
    lbl_image.config(image=tk_img)
    return lbl_image


def space(n):
    s = " "
    r = ""
    for i in range(n):
        r += s
    return r


def check_value_valid(mode, save_dir=None, url_path=None, keyword=None, page=None):
    if mode == 1:
        if not (save_dir and url_path):
            error_inform("请检查 论文保存文件夹 URL文件路径 是否已输入")
            return False
    elif mode == 2:
        if not (save_dir and keyword and page):
            error_inform("请检查 论文保存文件夹 关键词 下载页数范围 是否已输入")
            return False
    return True


def check_page_valid(page):
    page_comma = []
    try:
        if ',' in page:
            for item in page.split(","):
                if "-" in item:
                    pages = item.split("-")
                    if len(pages) != 2:
                        show_fail_window("下载页数范围输入错误")
                        return False, None
                    page_comma.extend([item for item in range(int(pages[0].strip()), int(pages[1].strip()) + 1)])
                else:
                    page_comma.append(int(item.strip()))

        elif "-" in page:
            pages = page.split("-")
            if len(pages) != 2:
                show_fail_window("下载页数范围输入错误")
                return False, None
            page_comma.extend([item for item in range(int(pages[0].strip()), int(pages[1].strip()) + 1)])
        else:
            page_comma.append(int(page.strip()))
    except Exception as e:
        show_fail_window("下载页数范围输入错误")
        return False, None
    page = sorted(list(set(page_comma)))
    for item in page:
        if item < 1:
            show_fail_window("下载页数范围输入错误")
            return False, None
    return True, page


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("%dx%d" % (900, 650))  # 窗体尺寸
        self.root.iconbitmap("img/root.ico")  # 窗体图标
        self.root.title("IEEE论文批量下载工具_v1.0")
        center_window(self.root)
        # self.root.resizable(False, False)          # 设置窗体不可改变大小
        self.no_title = False
        self.show_title()
        self.body()

    def body(self):

        # ---------------------------------------------------------------------
        # 标题栏
        # ---------------------------------------------------------------------
        f1 = tk.Frame(self.root)
        im1 = image_label(f1, "img/root.ico", 86, 86, False)
        im1.configure(bg="Teal")
        im1.bind('<Button-1>', self.show_title)
        im1.pack(side=tk.LEFT, anchor=tk.NW, fill=tk.Y)

        ft1 = tkFont.Font(family="微软雅黑", size=24, weight=tkFont.BOLD)
        tk.Label(f1, text="IEEE论文批量下载工具_v1.0", height=2, fg="white", font=ft1, bg="Teal") \
            .pack(side=tk.LEFT, expand=tk.YES, fill=tk.X)

        im2 = image_label(f1, "img/exit.ico", 86, 86, False)
        im2.configure(bg="Teal")
        im2.bind('<Button-1>', self.close)
        im2.pack(side=tk.RIGHT, anchor=tk.NW, fill=tk.Y)

        f2 = tk.Frame(self.root)
        img_content = image_label(f2, "img/ieee.png", width=400, height=142, keep_ratio=False).pack(padx=10, pady=10)
        f1.pack(fill=tk.X)
        f2.pack()

        ft_title = tkFont.Font(family="微软雅黑", size=13, weight=tkFont.BOLD)
        ft_middle = tkFont.Font(family="微软雅黑", size=11)
        ft = tkFont.Font(family="微软雅黑", size=13)
        ft_small = tkFont.Font(family="微软雅黑", size=6)

        f3 = tk.Frame(self.root)
        tk.Label(f3, text="论文保存文件夹 ", font=ft, anchor='w').pack(side='left', padx=60)
        self.save_dir = tk.Text(f3, bg="white", font=ft, height=1, width=50)
        self.save_dir.pack(side=tk.LEFT)
        f3.pack(fill='both', expand=True)

        f_empty = tk.Frame(self.root)
        tk.Label(f_empty, text="", font=ft_small).pack(side='left')
        f_empty.pack(fill='both', expand=True)

        # 模式1
        f5 = tk.Frame(self.root)
        tk.Label(f5, text="方法 1 : 使用URL.txt文件", font=ft_title, anchor='w').pack(side=tk.LEFT, padx=60)
        f5.pack(fill='both', expand=True)

        f_urltxt = tk.Frame(self.root)
        tk.Label(f_urltxt, text="URL文件路径", font=ft, anchor='w', padx=60).pack(side=tk.LEFT)
        self.url_txt_path = tk.Text(f_urltxt, bg="white", font=ft, height=1, width=40)
        self.url_txt_path.pack(side=tk.LEFT)
        tk.Button(f_urltxt, text="开始下载", width=10, height=1, bg="cadetblue", font=ft, command=self.begin_download_1) \
            .pack(side=tk.RIGHT, anchor=tk.W, padx=80)
        tk.Label(f_urltxt, text="", font=ft).pack(side=tk.LEFT)
        f_urltxt.pack(fill='both', expand=True)
        f9 = tk.Frame(self.root)
        self.CheckVar1 = tk.IntVar()
        self.save_with_yesr_1 = tk.Checkbutton(f9, text="论文保存时自动添加年份前缀", font=ft_middle, variable=self.CheckVar1,
                                               onvalue=1, offvalue=0)
        self.save_with_yesr_1.pack(side=tk.LEFT, padx=60)
        f9.pack(fill='both', expand=True)

        f_empty2 = tk.Frame(self.root)
        tk.Label(f_empty2, text="", font=ft_small).pack(side='left')
        f_empty2.pack(fill='both', expand=True)

        # 模式2
        f6 = tk.Frame(self.root)
        tk.Label(f6, text="方法 2 : 在线查询", font=ft_title, anchor='w').pack(side=tk.LEFT, padx=60)
        f6.pack(fill='both', expand=True)
        f7 = tk.Frame(self.root)
        tk.Label(f7, text="关键词", font=ft, anchor='w').pack(side=tk.LEFT, padx=60)
        self.keyword = tk.Text(f7, bg="white", font=ft, height=1, width=20)
        self.keyword.pack(side=tk.LEFT)
        tk.Label(f7, text="下载页数范围", font=ft, anchor='w').pack(side=tk.LEFT, padx=40)
        self.page_range = tk.Text(f7, bg="white", font=ft, height=1, width=10)
        self.page_range.pack(side=tk.LEFT, padx=0)
        tk.Button(f7, text="开始下载", width=10, height=1, bg="cadetblue", font=ft, command=self.begin_download_2) \
            .pack(side=tk.LEFT, anchor=tk.W, padx=40)
        f7.pack(fill='both', expand=True)

        f8 = tk.Frame(self.root)
        self.CheckVar2 = tk.IntVar()
        self.save_with_yesr_2 = tk.Checkbutton(f8, text="论文保存时自动添加年份前缀", font=ft_middle, variable=self.CheckVar2,
                                               onvalue=1, offvalue=0)
        self.save_with_yesr_2.pack(side=tk.LEFT, padx=60)
        f8.pack(fill='both', expand=True)

    def show_title(self, *args):
        self.root.overrideredirect(self.no_title)
        self.no_title = not self.no_title

    def download_1_thread(self):
        if show_begin_download("开始下载吗？"):
            save_dir = self.save_dir.get(0.0, tk.END).split("\n")[0].strip()
            url_txt_path = self.url_txt_path.get(0.0, tk.END).split("\n")[0].strip()
            save_with_year = self.CheckVar1.get()
            is_valid = check_value_valid(mode=1, save_dir=save_dir, url_path=url_txt_path)
            if not is_valid:
                return
            # 配置存储文件夹
            import os
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)
            status, paper_info = organize_info_by_txt(save_dir, url_txt_path, paper_name_with_year=save_with_year)
            if not status:
                show_fail_window("URL文件未找到...")
                return
            if self.all_downloaded(paper_info):
                info = "{}篇论文已存在，无需下载!".format(len(paper_info))
                show_succeed_window(info)
                return
            # 下载论文
            self.create_progress_bar(paper_info)  ## 创建progress bar窗口
            try:
                _thread.start_new_thread(self.refresh_window, ())
            except:
                show_fail_window("Error: 无法启动线程")
            succeed, paper_downloaded, already_exist = downLoad_paper(paper_info)
            if succeed:
                info = "成功下载{}篇论文！".format(paper_downloaded + already_exist)
                if hasattr(self, 'pb_window'):
                    self.pb_window.destroy()
                show_succeed_window(info)
            else:
                show_fail_window("下载失败，请检查配置。")

    def create_progress_bar(self, paper_info):
        if hasattr(self, 'pb_window'):
            self.pb_window.destroy()
        self.pb_window = tk.Toplevel()
        self.pb_window.geometry("300x140+600+300")
        self.pb_window.iconbitmap("img/root.ico")  # 窗体图标
        self.pb_window.title("下载进度")
        center_window(self.pb_window)
        self.download_pb = ttk.Progressbar(self.pb_window, length=200, mode="determinate", orient=tk.HORIZONTAL)
        self.download_pb.pack(padx=10, pady=20)
        self.download_pb["value"] = 0
        self.download_pb["maximum"] = len(paper_info)

    def refresh_window(self):
        if not hasattr(self, 'pb_window'):
            return
        if not hasattr(self, 'download_pb'):
            return
        while utils.get_value("progress_bar_num") < self.download_pb["maximum"]-1:
            if self.pb_window and self.download_pb:
                self.download_pb["value"] = utils.get_value("progress_bar_num")
                self.pb_window.update()
        if hasattr(self, 'pb_window'):
            self.pb_window.destroy()

    def begin_download_1(self):
        try:
            _thread.start_new_thread(self.download_1_thread, ())
        except:
            show_fail_window("Error: 无法启动线程")

    def all_downloaded(self, paperlist):
        for key, value in paperlist.items():
            if not os.path.exists(value['name']):
                return False
        return True

    def download_2_thread(self):
        if show_begin_download("开始下载吗？"):
            save_dir = self.save_dir.get(0.0, tk.END).split("\n")[0].strip()
            keywords = self.keyword.get(0.0, tk.END).split("\n")[0].strip()
            page_range = self.page_range.get(0.0, tk.END).split("\n")[0].strip()
            save_with_year = self.CheckVar2.get()
            is_valid = check_value_valid(mode=2, save_dir=save_dir, keyword=keywords, page=page_range)
            page_is_valid, page_range = check_page_valid(page_range)
            if not page_is_valid:
                return
            if not is_valid:
                return
            # 配置存储文件夹
            import os
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)
            status, paper_info = organize_info_by_query(keywords, page_range, save_dir, save_with_year)
            if not status:
                show_fail_window("URL解析失败...")

            if self.all_downloaded(paper_info):
                info = "{}篇论文已存在，无需下载!".format(len(paper_info))
                show_succeed_window(info)
                return
            # 下载论文
            self.create_progress_bar(paper_info)  ## 创建progress bar窗口
            try:
                _thread.start_new_thread(self.refresh_window, ())
            except:
                show_fail_window("Error: 无法启动线程")
            succeed, paper_downloaded, already_exist = downLoad_paper(paper_info, show_bar=True)
            if succeed:
                info = "成功下载{}篇论文!".format(paper_downloaded + already_exist)
                if hasattr(self, 'pb_window'):
                    self.pb_window.destroy()
                show_succeed_window(info)
            else:
                show_fail_window("下载失败，请检查配置。")

    def begin_download_2(self):
        try:
            _thread.start_new_thread(self.download_2_thread, ())
        except:
            show_fail_window("Error: 无法启动线程")

    def close(self, *arg):
        if show_confirm("确认退出吗 ?"):
            self.root.destroy()


if __name__ == "__main__":
    utils._init()
    utils.set_value("progress_bar_num", 0)
    app = App()
    app.root.mainloop()
