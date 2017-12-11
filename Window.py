from Snatch import Snatch
from tkinter import *
from tkinter import ttk
import threading

import socket
from time import *
# 全局变量
s = Snatch.socket_Snatch()
# 返回 时间 版本 协议 原地址 目标地址 长度
Host = socket.gethostbyname(socket.gethostname())


class App(object):

    def __init__(self, root):
        # 主机Ip
        self.Host = Host
        # 程序停止器
        self.boolen = False

        # 计算时间
        self.start_time = None
        self.stop_time = None

        # 过滤条件
        self.protocol = None
        self.src_ip = None
        self.det_ip = None

        self.data = []

        # 框架安装
        self.left_frame = Frame(root)
        self.left_frame.pack(side=LEFT)
        self.right_frame = Frame(root,)
        self.right_frame.pack(side=RIGHT)
        self.top_frame = Frame(self.right_frame, width=300, height=350,)
        self.top_frame.pack(side=TOP, fill=BOTH)
        self.bottom_frame = Frame(self.right_frame, width=300, height=60,)
        self.bottom_frame.pack(side=BOTTOM, fill=BOTH)

        self.Ip_label = Label(self.top_frame, text='本地IP：         ')
        self.Ip_label.grid(row=0, column=0)
        self.Ip_label_ = Label(self.top_frame, text=self.Host)
        self.Ip_label_.grid(row=0, column=1)

        self.start_time_label = Label(self.top_frame, text='开始时间：         ')
        self.start_time_label.grid(row=1,column=0)
        self.start_time_label_ = Label(self.top_frame, text='')
        self.start_time_label_.grid(row=1, column=1)

        self.end_time_label = Label(self.top_frame, text='结束时间：         ')
        self.end_time_label.grid(row=2, column=0)
        self.end_time_label_ = Label(self.top_frame, text='')
        self.end_time_label_.grid(row=2, column=1)

        # 秒数选择
        self.seconds_label = Label(self.top_frame, text='时间选择（秒）：     ')
        self.seconds_label.grid(row=3, column=0)

        Button(self.bottom_frame, text='开始',\
               command=self.start, width=20).grid(row=1, column=0)
        Button(self.bottom_frame, text='停止',\
               command=self.stop, width=20).grid(row=1, column=1)
        Button(self.bottom_frame, text='长度排序',\
               command=self.sort_by_len, width=20).grid(row=0, column=0)
        Button(self.bottom_frame, text='类型排序',\
               command=self.sort_by_ver, width=20).grid(row=0, column=1)
        Button(self.bottom_frame, text='清除数据',\
               command=self.clear, width=20).grid(row=2, column=0)

        self.secondsChosen = ttk.Combobox(self.top_frame, width=18,)
        self.secondsChosen['values'] = (0, 5, 10, 20, 60, 300)
        self.secondsChosen.grid(row=3, column=1)
        self.secondsChosen.current(0)

        # 用于区分 if 语句没什么设计含义
        if True:
            self.tree_data = ttk.Treeview(self.left_frame, show="headings", height=20,columns=("a", "b", "c", "d", "e",
                                                                                               "f"))
            self.vbar = ttk.Scrollbar(self.left_frame, orient=VERTICAL, command=self.tree_data.yview)
            # 定义树形结构与滚动条
            self.tree_data.configure(yscrollcommand=self.vbar.set)

            self.tree_data.column("a", width=200, anchor="center")
            self.tree_data.column("b", width=40, anchor="center")
            self.tree_data.column("c", width=40, anchor="center")
            self.tree_data.column("d", width=160, anchor="center")
            self.tree_data.column("e", width=160, anchor="center")
            self.tree_data.column("f", width=160, anchor="center")

            self.tree_data.heading("a", text="时间")
            self.tree_data.heading("b", text="版本")
            self.tree_data.heading("c", text="协议")
            self.tree_data.heading("d", text="源地址")
            self.tree_data.heading("e", text="目的地址")
            self.tree_data.heading("f", text="长度")

            self.tree_data.pack(side=LEFT, fill=BOTH, expand=1)
            self.vbar.pack(side=RIGHT, fill=Y)

    def stop(self):
        if self.boolen:
            self.boolen = False
            self.stop_time = time()
            self.end_time_label_.config(text=strftime('%Y-%m-%d %H:%M:%S', localtime(self.stop_time)))

    def start(self):
        self.boolen = True
        self.start_time = time()
        self.start_time_label_.config(text=strftime('%Y-%m-%d %H:%M:%S', localtime(self.start_time)))
        self.end_time_label_.config(text='')

        self.show()

    def show(self):
        if int(self.secondsChosen.get()) and time() > (self.start_time+int(self.secondsChosen.get())):
            self.stop()
        if self.boolen:
            self.data.append(Snatch.Receive(s))
            self.tree_data.insert("", 0, values=(self.data[-1][0], self.data[-1][1], self.data[-1][2], self.data[-1][3],
                                                 self.data[-1][4], self.data[-1][5]))
            self.tree_data.after(100, self.show)

    def clear(self):

        # 删除数据
        for x in map(self.tree_data.delete, self.tree_data.get_children("")):
            pass

    def sort_by_len(self):

        self.stop()
        self.data = sorted(self.data, key=lambda d: d[5])
        # print(self.data)
        # 删除数据
        for x in map(self.tree_data.delete, self.tree_data.get_children("")):
            pass
        # 重新插入
        for x in self.data:
            self.tree_data.insert("", 0, values=(x[0], x[1], x[2], x[3], x[4], x[5]))

    def sort_by_ver(self):

        self.stop()
        self.data = sorted(self.data, key=lambda d: d[2])
        # print(self.data)
        for x in map(self.tree_data.delete, self.tree_data.get_children("")):
            pass
        for x in self.data:
            self.tree_data.insert("", 0, values=(
                x[0], x[1], x[2], x[3], x[4], x[5]))


if __name__ == '__main__':
    root = Tk()
    root.title("CaoRui")
    app = App(root)
    root.mainloop()
