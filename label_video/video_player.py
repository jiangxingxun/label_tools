# coding:utf-8

from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import numpy as np
import threading
import cv2


class VideoFrame(ttk.Frame):
    def __init__(self, main, master, height=390, width=490,):
        super(VideoFrame, self).__init__(master, height=height, width=width)
        self.main_app = main
        self.image = None
        self.video = None
        self.file_path = ''
        self.first_add = True
        self.stop_event = threading.Event()
        self.threads = []
        self.button = []
        self.video_label = None
        self.create_interface()

    def create_interface(self):
        """创建视频播放模块界面"""
        screen_labelframe = ttk.Frame(self, height=300, width=500)
        screen_labelframe.pack()
        screen_labelframe.pack_propagate(0)
        self.video_label = ttk.Label(screen_labelframe, background='#1C1C1C', image=None)

        control_frame = ttk.Frame(self)
        control_frame.pack()
        play_button = ttk.Button(control_frame, text='play', width=15, command=self.start, state=DISABLED)  #
        play_button.pack(fill=Y, expand=YES, side='left', padx=15, pady=8)
        stop_button = ttk.Button(control_frame, text='stop', width=15, command=self.stop)
        stop_button.pack(fill=Y, expand=YES, side='left', padx=15, pady=8)
        self.button.append(play_button)
        self.button.append(stop_button)

    def process(self):
        """开始一个视频播放线程"""
        self.threads.clear()
        self.stop_event.clear()
        play_thread = threading.Thread(target=VideoFrame._play, args=(self,))
        play_thread.setDaemon(True)  # 守护线程
        play_thread.start()
        self.threads.append(play_thread)

    def load(self, path):
        """
        载入视频
        :param path: 视频路径
        :return:
        """
        self.file_path = path
        self.video_label.pack(fill=Y, expand=YES, side='bottom', padx=15, pady=8)
        self.process()

    def _renew(self, img):
        """
        刷新播放界面
        :param img:
        :return:
        """
        if isinstance(img, np.ndarray):
            img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        self.image = ImageTk.PhotoImage(image=img)
        self.video_label.configure(image=self.image)

    def _play(self):
        """播放视频线程函数"""
        self.video = cv2.VideoCapture(self.file_path)
        while self.video.isOpened():
            ret, frame = self.video.read()
            if ret is True and not self.stop_event.isSet():
                frame = self.resize_img(430, 250, frame)
                self._renew(frame)
                self.update_idletasks()
                self.update()
                self.master.update_idletasks()
                self.master.update()
                cv2.waitKey(5)
            else:
                break
        self.video.release()
        self.button[0]["state"] = NORMAL

    def resize_img(self, w_box, h_box, frame):
        """
        重新定义图像大小
        :param w_box: 显示框宽
        :param h_box: 显示框高
        :param frame: 读入图像
        :return: 调整大小的图像
        """
        h, w = frame.shape[:2]  # 获取图像的原始大小
        f1 = 1.0*w_box/w
        f2 = 1.0*h_box/h
        factor = min([f1, f2])
        width = int(w*factor)
        height = int(h*factor)
        size = (int(width), int(height))
        return cv2.resize(frame, size, interpolation=cv2.INTER_AREA)

    def start(self):
        """开始播放视频（在stop之后调用）"""
        if self.file_path == '':
            return
        self.button[0]["state"] = DISABLED
        self.main_app.next_Button[self.main_app.au_num]["state"] = DISABLED
        self.stop_event.set()
        self.stop_event.clear()
        self.process()

    def stop(self):
        """暂停退出视频"""
        self.stop_event.set()






