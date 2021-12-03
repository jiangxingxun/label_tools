# coding:utf-8

from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from PIL import Image
import json
import os
from video_player import VideoFrame

"""
标注软件
"""


def load_txt(root):
    """
    载入txt信息，将每行内容导入至list
    :param root: 路径
    :return: 已导入txt信息的list
    """
    lines = []
    with open(root, 'r') as file_to_read:
        while True:
            line = file_to_read.readline()
            if not line:
                break
            line = line.strip('\n')
            lines.append(line)
    return lines


class AppUI(object):
    def __init__(self, master=None):
        self.text_path = ''
        self.path = ''
        self.picture_path = []
        self.picture_name = []

        # 需要动态控制的button控件
        self.yes_Button = []
        self.no_Button = []
        self.next_Button = []

        # parameter
        self.title = load_txt('groundTruthClass.txt')  # 标签值导入
        self.pic_number = 0  # picture计数
        self.user_name = StringVar()
        self.user_age = StringVar()
        self.user_gender = StringVar()
        self.save_path = StringVar()
        self.au_number = StringVar()
        self.activation = ""
        self.au_num = 0

        self.root = master
        self.root.title("Emotion Annotation for videos")
        self.root.geometry("+0+0")  # 不加这句，跳转到主界面，位置不对

        # 左frame设置
        left_frame = Frame(self.root)
        left_frame.pack(fill=Y, expand=YES, side=LEFT, padx=15, pady=8)

        # 右frame设置
        right_frame = Frame(self.root)
        right_frame.pack(fill=Y, expand=YES, side=LEFT, padx=15, pady=8)

        # 模块生成
        self.create_menu(self.root)
        self.create_introduction(left_frame)
        self.parameter_labelframe = self.create_parameter(right_frame)
        self.picture_labelframe = self.create_picture(left_frame)
        self.operate_labelframe = self.create_operate(right_frame)

        # 大小设置
        # self.root.resizable(False, False)  # 调用方法会禁止根窗体改变大小
        # scn_width, scn_height = self.root.maxsize()
        scn_width, scn_height = 1100, 630  # get screen width and height
        cur_width = self.root.winfo_screenwidth()
        cur_height = self.root.winfo_screenheight()
        size = '%dx%d+%d+%d' % (scn_width, scn_height, (cur_width - scn_width) / 2, (cur_height - scn_height) / 2)
        self.root.geometry(size)

    # 界面生成函数
    def create_menu(self, root):
        """
        创建菜单栏
        :param root:上级模块
        :return:
        """
        menu = Menu(root)

        # 创建二级菜单
        file_menu = Menu(menu, tearoff=0)
        file_menu.add_command(label="Set path", command=self.open_dir)
        file_menu.add_separator()

        # scan_menu = Menu(menu)
        file_menu.add_command(label="Scan")

        about_menu = Menu(menu, tearoff=0)
        about_menu.add_command(label="version:1.0")

        # 在菜单栏中添加以下一级菜单
        menu.add_cascade(label="Files", menu=file_menu)
        menu.add_cascade(label="About", menu=about_menu)
        root['menu'] = menu

    def create_introduction(self, root):
        """
        创建introduction模块
        :param root: 上级模块
        :return:
        """
        lf_introduction = ttk.LabelFrame(root, height=100, width=100, text="Introduction")
        lf_introduction.pack(fill=X, expand=YES, side='top', padx=15, pady=8)

        # 导入introduction内容
        introduction_text = load_txt('introduction.txt')
        for i in range(len(introduction_text)):
            ttk.Label(lf_introduction, text=introduction_text[i]).pack(fill=X, expand=YES, side='top', padx=15, pady=8)

    def create_parameter(self, root):
        """
         创建parameter模块
         :param root: 上级模块
         :return: parameter模块
        """
        lf_parameter = ttk.LabelFrame(root, height=100, width=100, text="Parameter")
        lf_parameter.pack(fill=X, expand=YES, side='top', padx=15, pady=8)

        # 创建user_frame模块
        user_frame = Frame(lf_parameter)
        user_frame.pack(fill=X, expand=YES, side=TOP, padx=15, pady=8)

        # user_frame：Name录入
        ttk.Label(user_frame, text="Name").pack(side='left', padx=15, pady=8)
        ttk.Entry(user_frame, textvariable=self.user_name, width=7).pack(side='left')

        # user_frame：Age录入
        ttk.Label(user_frame, text="Age").pack(side='left', padx=15, pady=8)
        ttk.Entry(user_frame, textvariable=self.user_age, width=7).pack(side='left')

        # user_frame：Gender录入
        ttk.Label(user_frame, text="Gender").pack(side='left', padx=15, pady=8)
        self.user_gender.set("Male")
        an_om = ttk.OptionMenu(user_frame, self.user_gender, "", "Male", "Female")
        an_om.pack(side='left', padx=15, pady=8)

        # 创建save_frame模块
        save_frame = Frame(lf_parameter)
        save_frame.pack(fill=X, expand=YES, side=TOP, padx=15, pady=8)

        # save_frame：保存路径确定
        ttk.Label(save_frame, text="Output").pack(side='left', padx=15, pady=8)
        ttk.Entry(save_frame, textvariable=self.save_path, width=25).pack(side='left', padx=15, pady=8)
        ttk.Button(save_frame, text="...", width=3, command=self.save_file).pack(side='left', padx=15, pady=8)

        # 创建au_frame模块
        au_frame = Frame(lf_parameter)
        au_frame.pack(fill=X, expand=YES, side=TOP, padx=15, pady=8)

        # au_frame：au选择
        options = [""]
        options.extend(["Emotion"])
        self.au_number.set(options[1])
        ttk.Label(au_frame, text="Choose Type").pack(side='left', padx=15, pady=8)
        an_om = ttk.OptionMenu(au_frame, self.au_number, *options)
        an_om.pack(side='left', padx=37, pady=8)

        # 创建load_frame模块
        load_frame = Frame(lf_parameter)
        load_frame.pack(fill=X, expand=YES, side=TOP, padx=15, pady=8)

        # load_frame：开始导入
        ttk.Button(load_frame, text="OK", width=15, command=self.on_ok).pack(side='left', padx=15, pady=8)
        ttk.Button(load_frame, text="Start Load", width=15, command=self.open_file).pack(side='left', padx=15, pady=8)

        return lf_parameter

    def event_handler(self, event):
        """
        键盘响应函数
        :param event: 键盘事件
        :return:
        """
        if event.keysym == 'Left':
            self.yes_Button[self.au_num].invoke()
        elif event.keysym == 'Right':
            self.no_Button[self.au_num].invoke()
        elif event.keysym == 'Shift_L':
            self.next_Button[self.au_num].invoke()

        # 创建au_frame模块
        au_frame = Frame(lf_parameter)
        au_frame.pack(fill=X, expand=YES, side=TOP, padx=15, pady=8)

        # au_frame：au选择
        options = [""]
        options.extend(["emotion"])
        self.au_number.set(options[1])
        ttk.Label(au_frame, text="Choose Type").pack(side='left', padx=15, pady=8)
        an_om = ttk.OptionMenu(au_frame, self.au_number, *options)
        an_om.pack(side='left', padx=37, pady=8)

        # 创建load_frame模块
        load_frame = Frame(lf_parameter)
        load_frame.pack(fill=X, expand=YES, side=TOP, padx=15, pady=8)

        # load_frame：开始导入
        ttk.Button(load_frame, text="OK", width=15, command=self.on_ok).pack(side='left', padx=15, pady=8)
        ttk.Button(load_frame, text="Start Load", width=15, command=self.open_file).pack(side='left', padx=15, pady=8)

        return lf_parameter

    def create_picture(self, root):
        """
        创建picture模块
        :param root: 上级模块
        :return: picture模块
        """
        lf_picture = ttk.LabelFrame(root, height=400, width=500, text="Video")
        lf_picture.pack(fill=X, expand=YES, side='top', padx=15, pady=8)
        lf_picture.pack_propagate(0)

        global num_label
        num_label = ttk.Label(lf_picture, text='num:')
        num_label.pack()

        global video_frame
        video_frame = VideoFrame(main=self, master=lf_picture, height=390, width=490)
        video_frame.pack(fill=X, expand=YES, side='bottom', padx=15, pady=8)

        return lf_picture

    def create_operate(self, root):
        """
        创建operate模块
        :param root: 上级模块
        :return: operate模块
        """
        lf_operate = ttk.LabelFrame(root, height=100, width=100, text="Operate")
        lf_operate.pack(fill=X, expand=YES, side='top', padx=15, pady=40)

        # 绑定键盘
        lf_operate.focus_set()
        lf_operate.bind_all(sequence='<KeyPress>', func=self.event_handler)
        style = ttk.Style()
        style.configure("ON.TButton", foreground="black", background="red")
        style.configure("OFF.TButton", foreground="black", background="white")

        # yes，no，next，button生成
        ttk.Label(lf_operate, text=self.title[0]).grid(row=0, column=0, padx=15, pady=8)
        button = ttk.Button(lf_operate, text="1", width=3, state=DISABLED, command=self.on_yes_1)
        self.yes_Button.append(button)
        button.grid(row=0, column=1, padx=5, pady=8)

        ttk.Label(lf_operate, text=self.title[1]).grid(row=1, column=0, padx=15, pady=8)
        button = ttk.Button(lf_operate, text="2", width=3, state=DISABLED, command=self.on_yes_2)
        self.yes_Button.append(button)
        button.grid(row=1, column=1, padx=5, pady=8)

        ttk.Label(lf_operate, text=self.title[2]).grid(row=2, column=0, padx=15, pady=8)
        button = ttk.Button(lf_operate, text="3", width=3, state=DISABLED, command=self.on_yes_3)
        self.yes_Button.append(button)
        button.grid(row=2, column=1, padx=5, pady=8)

        ttk.Label(lf_operate, text=self.title[3]).grid(row=0, column=2, padx=15, pady=8)
        button = ttk.Button(lf_operate, text="4", width=3, state=DISABLED, command=self.on_yes_4)
        self.yes_Button.append(button)
        button.grid(row=0, column=3, padx=5, pady=8)

        ttk.Label(lf_operate, text=self.title[4]).grid(row=1, column=2, padx=15, pady=8)
        button = ttk.Button(lf_operate, text="5", width=3, state=DISABLED, command=self.on_yes_5)
        self.yes_Button.append(button)
        button.grid(row=1, column=3, padx=5, pady=8)

        ttk.Label(lf_operate, text=self.title[5]).grid(row=2, column=2, padx=15, pady=8)
        button = ttk.Button(lf_operate, text="6", width=3, state=DISABLED, command=self.on_yes_6)
        self.yes_Button.append(button)
        button.grid(row=2, column=3, padx=5, pady=8)

        ttk.Label(lf_operate, text=self.title[6]).grid(row=0, column=4, padx=15, pady=8)
        button = ttk.Button(lf_operate, text="7", width=3, state=DISABLED, command=self.on_yes_7)
        self.yes_Button.append(button)
        button.grid(row=0, column=5, padx=5, pady=8)

        button = ttk.Button(lf_operate, text="Next", width=5, state=DISABLED, command=self.next_img)
        self.next_Button.append(button)
        button.grid(row=1, column=5, padx=5, pady=8)

        return lf_operate

    # 功能函数
    def save_file(self):
        """保存文件对话框生成"""
        path = filedialog.asksaveasfilename(title=u'保存文件', filetypes=[("TextFile", ".txt")])
        if path:
            self.text_path = path
            self.save_path.set(self.text_path)
            self.parameter_labelframe.update_idletasks()
            file = open(self.text_path, 'a')
            file.close()

    def open_file(self):
        """打开文件对话框生成"""
        video_frame.stop()
        default_dir = r"文件路径"
        path = filedialog.askopenfilenames(title=u'选择文件', initialdir=(os.path.expanduser(default_dir)),
                                           filetypes=[("MP4", ".mp4"), ("AVI", ".avi"), ("RMVB", ".rmvb"),
                                                      ("WMV", ".wmv"), ("MKV", ".mkv")])
        if path:
            self.picture_path = path
            self.pic_number = 0
            self.show_img()
            num_label.configure(text='num:' + str(self.pic_number + 1) + '/' + str(len(self.picture_path)))

    def load_picture(self, file_dir):
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                if os.path.splitext(file)[1] == '.mp4'or \
                        os.path.splitext(file)[1] == '.avi'or \
                        os.path.splitext(file)[1] == '.rmvb':
                    self.picture_path.append(os.path.join(root, file))
                    self.picture_name.append(file[0])

    def open_dir(self):
        """打开路径设置"""
        d = filedialog.Directory()
        self.path = d.show(initialdir=self.path)

    def show_img(self):
        """初始化显示图像"""
        global video_frame
        if len(self.picture_path) == 0:
            return
        video_frame.load(self.picture_path[self.pic_number])

    def resize_img(self, w_box, h_box, pil_image):
        """
        重新定义图像大小
        :param w_box: 显示框宽
        :param h_box: 显示框高
        :param pil_image: pil读入图像
        :return: 调整大小的pil图像
        """
        w, h = pil_image.size  # 获取图像的原始大小
        f1 = 1.0*w_box/w
        f2 = 1.0*h_box/h
        factor = min([f1, f2])
        width = int(w*factor)
        height = int(h*factor)
        return pil_image.resize((width, height), Image.ANTIALIAS)

    def next_img(self):
        """下一张图像显示"""
        self.write_json()
        self.next_Button[self.au_num]["state"] = DISABLED
        if len(self.picture_path) == 0:
            return
        global video_frame
        if self.pic_number == len(self.picture_path)-1:
            messagebox.showinfo("Warning", "This is the last picture")
            self.pic_number += 1
            return
        video_frame.button[0]["state"] = DISABLED
        self.pic_number += 1
        video_frame.load(self.picture_path[self.pic_number])
        num_label.configure(text='num:' + str(self.pic_number + 1) + '/' + str(len(self.picture_path)))
        self.yes_Button[self.au_num].configure(style="OFF.TButton")

    def last_img(self):
        """上一张图像显示"""
        if len(self.picture_path) == 0:
            return
        global video_frame
        if self.pic_number == 0:
            messagebox.showinfo("Warning", "This is the first picture")
            return
        video_frame.button[0]["state"] = DISABLED
        self.pic_number -= 1
        video_frame.load(self.picture_path[self.pic_number])
        num_label.configure(text='num:' + str(self.pic_number + 1) + '/' + str(len(self.picture_path)))
        self.picture_labelframe.update_idletasks()

    def text_write(self, full_path, msg):
        """
        写txt文件
        :param full_path: txt路径
        :param msg: 写入信息
        :return:
        """
        file = open(full_path, 'a')
        file.write(msg)   # msg也就是下面的Hello world!
        file.close()

    def write_json(self):
        """将标记信息以json格式写入txt"""
        m_dict = {}
        # 提取文件名
        (file_path, temp_filename) = os.path.split(self.picture_path[self.pic_number])
        (filename, extension) = os.path.splitext(temp_filename)
        # 更新字典
        m_dict.update(name=self.user_name.get(), age=self.user_age.get(), gender=self.user_gender.get(),
                      file_name=filename, pic_number=str(self.pic_number), emotion_value=self.activation, repeat="1")
        m_json = json.dumps(m_dict)
        self.text_write(self.text_path, m_json + '\n')

    def active_operate_button(self):
        """Yes,No,Next按钮动态激活"""
        for i in range(7):
            self.yes_Button[i]["state"] = NORMAL
        self.next_Button[0]["state"] = DISABLED

    def on_yes_1(self):
        """Yes响应函数，标记activation为1"""
        if len(self.picture_path) is 0:
            messagebox.showinfo("Warning", "No picture load in")
            return
        if self.pic_number == len(self.picture_path):
            messagebox.showinfo("Warning", "This is the last picture")
            return
        self.activation = "1"
        video_frame.stop()
        self.next_Button[0]["state"] = NORMAL
        for i in range(7):
            self.yes_Button[i].configure(style="OFF.TButton")
        self.yes_Button[0].configure(style="ON.TButton")

    def on_yes_2(self):
        """Yes响应函数，标记activation为1"""
        if len(self.picture_path) is 0:
            messagebox.showinfo("Warning", "No picture load in")
            return
        if self.pic_number == len(self.picture_path):
            messagebox.showinfo("Warning", "This is the last picture")
            return
        self.activation = "2"
        video_frame.stop()
        self.next_Button[0]["state"] = NORMAL
        for i in range(7):
            self.yes_Button[i].configure(style="OFF.TButton")
        self.yes_Button[1].configure(style="ON.TButton")

    def on_yes_3(self):
        """Yes响应函数，标记activation为1"""
        if len(self.picture_path) is 0:
            messagebox.showinfo("Warning", "No picture load in")
            return
        if self.pic_number == len(self.picture_path):
            messagebox.showinfo("Warning", "This is the last picture")
            return
        self.activation = "3"
        video_frame.stop()
        self.next_Button[0]["state"] = NORMAL
        for i in range(7):
            self.yes_Button[i].configure(style="OFF.TButton")
        self.yes_Button[2].configure(style="ON.TButton")

    def on_yes_4(self):
        """Yes响应函数，标记activation为1"""
        if len(self.picture_path) is 0:
            messagebox.showinfo("Warning", "No picture load in")
            return
        if self.pic_number == len(self.picture_path):
            messagebox.showinfo("Warning", "This is the last picture")
            return
        self.activation = "4"
        video_frame.stop()
        self.next_Button[0]["state"] = NORMAL
        for i in range(7):
            self.yes_Button[i].configure(style="OFF.TButton")
        self.yes_Button[3].configure(style="ON.TButton")

    def on_yes_5(self):
        """Yes响应函数，标记activation为1"""
        if len(self.picture_path) is 0:
            messagebox.showinfo("Warning", "No picture load in")
            return
        if self.pic_number == len(self.picture_path):
            messagebox.showinfo("Warning", "This is the last picture")
            return
        self.activation = "5"
        video_frame.stop()
        self.next_Button[0]["state"] = NORMAL
        for i in range(7):
            self.yes_Button[i].configure(style="OFF.TButton")
        self.yes_Button[4].configure(style="ON.TButton")

    def on_yes_6(self):
        """Yes响应函数，标记activation为1"""
        if len(self.picture_path) is 0:
            messagebox.showinfo("Warning", "No picture load in")
            return
        if self.pic_number == len(self.picture_path):
            messagebox.showinfo("Warning", "This is the last picture")
            return
        self.activation = "6"
        video_frame.stop()
        self.next_Button[0]["state"] = NORMAL
        for i in range(7):
            self.yes_Button[i].configure(style="OFF.TButton")
        self.yes_Button[5].configure(style="ON.TButton")

    def on_yes_7(self):
        """Yes响应函数，标记activation为1"""
        if len(self.picture_path) is 0:
            messagebox.showinfo("Warning", "No picture load in")
            return
        if self.pic_number == len(self.picture_path):
            messagebox.showinfo("Warning", "This is the last picture")
            return
        self.activation = "7"
        video_frame.stop()
        self.next_Button[0]["state"] = NORMAL
        for i in range(7):
            self.yes_Button[i].configure(style="OFF.TButton")
        self.yes_Button[6].configure(style="ON.TButton")

    def on_ok(self):
        """OK响应函数，用于检查信息，激活按钮"""
        if self.user_name.get() == "":
            messagebox.showinfo("Incomplete Information", "Please fill in your name")
            return
        if self.user_age.get() == "":
            messagebox.showinfo("Incomplete Information", "Please fill in your age")
            return
        if self.save_path.get() == "":
            messagebox.showinfo("Incomplete Information", "Please fill in save path")
            return
        self.active_operate_button()

    def event_handler(self, event):
        """
        键盘响应函数
        :param event: 键盘事件
        :return:
        """
        if event.keysym == '1':
            self.yes_Button[0].invoke()
        elif event.keysym == '2':
            self.yes_Button[1].invoke()
        elif event.keysym == '3':
            self.yes_Button[2].invoke()
        elif event.keysym == '4':
            self.yes_Button[3].invoke()
        elif event.keysym == '5':
            self.yes_Button[4].invoke()
        elif event.keysym == '6':
            self.yes_Button[5].invoke()
        elif event.keysym == '7':
            self.yes_Button[6].invoke()
        elif event.keysym == 'n':
            self.next_Button[self.au_num].invoke()


if __name__ == '__main__':
    root = Tk()
    AppUI(root)
    root.mainloop()



