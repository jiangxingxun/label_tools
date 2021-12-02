# coding:utf8

# register.py
# 功能说明：用户运行程序后，自动检测认证状态，如果未经认证，就需要注册。
# 注册过程是用户将程序运行后显示的机器码（卷序号）发回给管理员，
# 管理员通过加密后生成加密文件或字符串给回用户。
# 每次登录，在有注册文件或者注册码的情况下，软件就会通过DES和base64解码，
# 如果解码后和重新获取的机器码一致，则通过认证，进入主程序。

import base64
import win32api
from pyDes import *
from tkinter import messagebox
from tkinter import *
from tkinter import ttk


class Register:
    def __init__(self):
        self.Des_Key = b"BHC#@*UM"  # Key
        self.Des_IV = b"\x22\x33\x35\x81\xBC\x38\x5A\xE7"  # 自定IV向量

    # 获取C盘卷序列号
    # 使用C盘卷序列号的优点是长度短，方便操作，比如1513085707，但是对C盘进行格式化或重装电脑等操作会影响C盘卷序列号。
    # win32api.GetVolumeInformation(Volume Name, Volume Serial Number, Maximum Component
    # Length of a file name, Sys Flags, File System Name)
    # return('', 1513085707, 255, 65470719, 'NTFS'),volume serial number is  1513085707.
    def getCVolumeSerialNumber(self):
        CVolumeSerialNumber = win32api.GetVolumeInformation("C:\\")[1]
        # print chardet.detect(str(CVolumeSerialNumber))
        # print CVolumeSerialNumber
        if CVolumeSerialNumber:
            return str(
                CVolumeSerialNumber)  # number is long type，has to be changed to str for comparing to content after.
        else:
            return 0

    # 使用DES加base64的形式加密
    # 考虑过使用M2Crypto和rsa，但是都因为在windows环境中糟糕的安装配置过程而放弃
    def DesEncrypt(self, str):
        k = des(self.Des_Key, CBC, self.Des_IV, pad=None, padmode=PAD_PKCS5)
        EncryptStr = k.encrypt(str)
        # EncryptStr = binascii.unhexlify(k.encrypt(str))
        return base64.b64encode(EncryptStr)  # 转base64编码返回

    # des解码
    def DesDecrypt(self, str):
        k = des(self.Des_Key, CBC, self.Des_IV, pad=None, padmode=PAD_PKCS5)
        DecryptStr = k.decrypt(str)
        # DecryptStr = a2b_hex(k.decrypt(str))
        # print(DecryptStr)
        return bytes.decode(DecryptStr)

    # 获取注册码，验证成功后生成注册文件
    def regist(self):
        key = input('please input your register code: ')
        # 由于输入类似“12”这种不符合base64规则的字符串会引起异常，所以需要增加输入判断
        # while key

        if key:
            content = self.getCVolumeSerialNumber()  # number has been changed to str type after use str()
            # print chardet.detect(content)
            # print type(content)
            # print content
            # type(key_decrypted) is str
            key_decrypted = str(self.DesDecrypt(base64.b64decode(key)))
            # print chardet.detect(key_decrypted)
            # print key_decrypted
            # type(key_decrypted) is str
            if content != 0 and key_decrypted != 0:
                if content != key_decrypted:
                    print("wrong register code, please check and input your register code again:")
                    self.regist()
                elif content == key_decrypted:
                    print("register succeed.")
                    # 读写文件要加判断
                    with open('./register', 'w') as f:
                        f.write(key)
                        f.close()
                    return True
                else:
                    return False
            else:
                return False
        else:
            self.regist()
        return False

    def checkAuthored(self):
        content = self.getCVolumeSerialNumber()
        checkAuthoredResult = 0
        # 读写文件要加判断
        try:
            f = open('./register', 'r')
            if f:
                key = f.read()
                if key:
                    key_decrypted = self.DesDecrypt(base64.b64decode(key))
                    if key_decrypted:
                        if key_decrypted == content:
                            checkAuthoredResult = 1
                        else:
                            checkAuthoredResult = -1
                    else:
                        checkAuthoredResult = -2
                else:
                    checkAuthoredResult = -3
            else:
                self.regist()
        except IOError:
            self.regist()
        print(checkAuthoredResult)
        return checkAuthoredResult


class AdminRegisterApp(Register):
    def __init__(self, master=None):
        super(AdminRegisterApp, self).__init__()
        self.page = None
        self.root = master

        self.serial_number = StringVar()
        self.register_code = StringVar()

        self.root.title("管理员注册机")
        self.create_page(self.root)

        # 大小设置
        self.root.resizable(False, False)  # 调用方法会禁止根窗体改变大小
        scn_width, scn_height = 400, 180  # get screen width and height
        cur_width = self.root.winfo_screenwidth()
        cur_height = self.root.winfo_screenheight()
        size = '+%d+%d' % ((cur_width - scn_width) / 2, (cur_height - scn_height) / 2)
        self.root.geometry(size)

    def create_page(self, master):
        self.page = ttk.Frame(master)  # 创建Frame
        self.page.pack(fill=Y, expand=YES, side=LEFT, padx=15, pady=8)
        ttk.Label(self.page, text='C盘卷序列号: ').grid(row=1, stick=W, pady=10)
        ttk.Entry(self.page, textvariable=self.serial_number, width=35).grid(row=1, column=1, stick=E)
        ttk.Label(self.page, text='注册码: ').grid(row=2, stick=W, pady=10)
        ttk.Entry(self.page, textvariable=self.register_code, width=35).grid(row=2, column=1, stick=E)
        ttk.Button(self.page, text='获取注册码', command=self.get_password, width=15).grid(row=3, column=1, stick=E, pady=8)

    def get_password(self):
        content = self.serial_number.get()
        if content is '':
            messagebox.showinfo("Warning", "no serial number")
            return
        key = self.DesEncrypt(str(content))
        self.register_code.set(key)


if __name__ == '__main__':
    # register = Register()
    # print(register.DesEncrypt('-395238789'))  # K9NveRW8migV1BXLi6HP4w==   -395238789
    root = Tk()
    AdminRegisterApp(root)
    root.mainloop()


