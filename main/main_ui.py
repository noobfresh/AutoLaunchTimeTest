# coding=utf-8
import ttk
from Tkinter import Frame, YES, BOTH, Label, TOP, Entry, LEFT, Button, END
from tkFileDialog import askdirectory, askopenfilenames

from tkinter import filedialog

from config.configs import Config
from config.configs2 import Config2
from main import start, startAppWithConfig


class Params:

    def __init__(self):
        self.install_method = "手动安装"  # 安装方式
        self.first_start_times = "1"  # 首次启动次数
        self.normal_start_times = "1"  # 正常启动次数
        self.enter_liveroom_times = "1"  # 进入直播间次数
        self.app_name = "yy"  # app名称
        self.package_name = "com.duowan.mobile"  # 包名
        self.app_path = "F:"  # 安装包地址
        self.video_path = "F:"  # 视频地址
        self.features = "F:"  # 特征图
        self.sdk_path = "SDK路径"  # sdk路径


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master, bg='black')
        self.pack(expand=YES, fill=BOTH)
        self.window_init()
        self.createWidgets()
        # self.doSomething()

    def window_init(self):
        self.master.title('自动化测试脚本')
        self.master.bg = 'black'
        width, height = self.master.maxsize()
        self.master.geometry("{}x{}".format(width >> 1, height >> 1))

    def startApp(self):
        print 'sdk = ' + self.videoPathEntry.get()
        params = Params()
        params.sdk_path = self.sdkPath
        params.video_path = self.videoPath
        params.install_method = self.install_method
        params.first_start_times = self.first_start_times
        params.normal_start_times = self.normal_start_times
        params.enter_liveroom_times = self.enter_liveroom_times
        params.app_name = self.app_name
        params.package_name = self.package_name
        params.app_path = self.app_path
        params.features = self.features

        startAppWithConfig(params)
        # start()

    def clickListener(self, event):
        print self.combox.get()

    def btnSdkBtnClick(self):
        self.sdkPath = askdirectory()
        self.sdkPathEntry.delete(0, END)
        self.sdkPathEntry.insert(0, self.sdkPath)
        if self.sdkPath != "":
            Config2("default.ini").update("default", "sdk_path", self.sdkPath)

    def btnVideoBtnClick(self):
        self.videoPath = askopenfilenames()
        self.videoPathEntry.delete(0, END)
        self.videoPathEntry.insert(0, self.videoPath)
        self.videoPath = self.sdkPathEntry.get()
        # if videoPath != "":
        #     Config2("default.ini").update("default", "sdk_path", videoPath)

    def initConfig(self):
        conf = Config("default.ini")
        self.sdkPath = conf.getconf("default").sdk_path  # sdk路径
        self.sdkPathEntry.delete(0, END)
        self.sdkPathEntry.insert(0, self.sdkPath)
        # videoPath = conf.getconf("default").sdk_path
        # self.sdkPathEntry.delete(0, END)
        # self.sdkPathEntry.insert(0, sdkPath)
        self.install_method = self.combox.get()  # 安装方式
        self.first_start_times = conf.getconf("default").first_start  # 首次启动次数
        self.normal_start_times = conf.getconf("default").normal_start  # 正常启动次数
        self.enter_liveroom_times = conf.getconf("default").enter_liveroom  # 进入直播间次数
        self.app_name = conf.getconf("default").app_name  # app名称
        self.package_name = conf.getconf("default").package  # 包名
        self.app_path = ""  # 安装包地址
        self.features = ""  # 特征图

    def createWidgets(self):
        # fm1
        self.fm1 = Frame(self, bg='black')
        self.titleLabel = Label(self.fm1, text="自动化测试脚本", font=('微软雅黑', 24), fg="white", bg='black')
        self.titleLabel.pack()
        self.fm1.pack(side=TOP, expand=YES, fill='x', pady=20)

        # fm2
        self.fm2 = Frame(self, bg='black')
        self.fm2_left = Frame(self.fm2, bg='black')
        self.fm2_right = Frame(self.fm2, bg='black')
        self.fm2_left_top = Frame(self.fm2_left, bg='black')
        self.fm2_left_mid = Frame(self.fm2_left, bg='black')
        self.fm2_left_bottom = Frame(self.fm2_left, bg='black')

        ## -----------------------------------------------------------------------------------------
        self.sdkPathEntry = Entry(self.fm2_left_top, font=('微软雅黑', 10), width='30', fg='#FF4081')
        self.sdkPathBtn = Button(self.fm2_left_top, text='SDK路径', bg='#22C9C9', fg='white',
                                 font=('微软雅黑', 10), width='16', command=self.btnSdkBtnClick)

        self.videoPathEntry = Entry(self.fm2_left_bottom, font=('微软雅黑', 12), width='30', fg='#22C9C9')
        self.videoPathButton = Button(self.fm2_left_bottom, text='上传视频', bg='#22C9C9', fg='white',
                                      font=('微软雅黑', 10), width='16', command=self.btnVideoBtnClick)

        self.startModeLabel = Label(self.fm2_left_mid, text='启动方式', bg='#22C9C9', fg='white',
                                    font=('微软雅黑', 10), width='16', )

        # 创建下拉菜单
        self.combox = ttk.Combobox(self.fm2_left_mid)
        self.combox['value'] = ('手动启动', '自动启动')
        self.combox.current(0)
        self.combox.bind("<<ComboboxSelected>>", self.clickListener)

        self.startAppBtn = Button(self.fm2_right, text='启动脚本', bg='black', fg='white',
                                  command=self.startApp)

        ## -----------------------------------------------------------------------------------------
        self.fm2.pack(side=TOP, expand=YES, fill="y")
        self.fm2_left.pack(side=TOP, pady=10, fill='x')
        self.fm2_left_top.pack(side=TOP, padx=60, pady=20, expand=YES, fill='x')
        self.fm2_left_mid.pack(side=TOP, padx=60, pady=20, expand=YES, fill='x')
        self.fm2_left_bottom.pack(side=LEFT, padx=60, pady=20, expand=YES, fill='x')
        self.startModeLabel.pack(side=LEFT)
        self.combox.pack(side=LEFT, padx=20)
        self.sdkPathBtn.pack(side=LEFT)
        self.sdkPathEntry.pack(side=LEFT, fill='y', padx=20)
        self.videoPathButton.pack(side=LEFT)
        self.videoPathEntry.pack(side=LEFT, fill='y', padx=20)

        self.fm2_right.pack(side=TOP, pady=10, fill='x')
        self.startAppBtn.pack(side=TOP, expand=YES, fill='y')


if __name__ == '__main__':
    app = Application()

    app.initConfig()

    app.mainloop()
