# coding=utf-8
import ttk
from Tkinter import Frame, YES, BOTH, Label, TOP, Entry, LEFT, Button, END
from tkFileDialog import askdirectory, askopenfilenames

from config.configs import Config
from config.configs2 import Config2
from main import startAppWithConfig


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

    def window_init(self):
        self.master.title('自动化测试脚本')
        self.master.bg = 'black'
        width, height = self.master.maxsize()
        self.master.geometry("{}x{}".format(width >> 1, height >> 1))

    def collectParams(self):
        params = Params()
        params.sdk_path = self.sdkPath
        params.video_path = self.videoPath
        params.install_method = self.installMethos
        params.first_start_times = self.firstStartTime
        params.normal_start_times = self.normaStartTime
        params.enter_liveroom_times = self.enterLiveRoonTime
        params.app_name = self.appName
        params.package_name = self.packageName
        params.app_path = self.appPath
        params.features = self.features
        return params

    def saveToConfig(self):

        if self.sdkPathEntry.get() != "":
            Config2("default.ini").update("default", "sdk_path", self.sdkPathEntry.get())

        if self.videoPathEntry.get() != "":
            Config2("default.ini").update("default", "sdk_path", self.videoPathEntry.get())

        if self.firstStartEntry.get() != "":
            Config2("default.ini").update("default", "first_start", self.firstStartEntry.get())

        if self.normalStartEntry.get() != "":
            Config2("default.ini").update("default", "normal_start", self.normalStartEntry.get())

        if self.enterLiveRoomEntry.get() != "":
            Config2("default.ini").update("default", "enter_liveroom", self.enterLiveRoomEntry.get())

        if self.appNameEntry.get() != "":
            Config2("default.ini").update("default", "app_name", self.appNameEntry.get())

        if self.packageNameEntry.get() != "":
            Config2("default.ini").update("default", "package", self.packageNameEntry.get())

        if self.appPathEntry.get() != "":
            Config2("default.ini").update("default", "app_path", self.appPathEntry.get())

    def startAppBtnClickListener(self):
        self.saveToConfig()
        startAppWithConfig(self.collectParams())

    def comboxItemListener(self, event):
        if self.combox.get() == "自动安装":
            self.installMethos = 1
        else:
            self.installMethos = 2

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

    def btnAppPathBtnClick(self):
        self.appPath = askopenfilenames()
        self.appPathEntry.delete(0, END)
        self.appPathEntry.insert(0, self.appPath)
        if self.appPath != "":
            Config2("default.ini").update("default", "app_path", self.appPath)

    def btnPackageBtnClick(self):
        print "click"

    def btnAppNameClick(self):
        print "click"

    def btnfirstStartClick(self):
        print "click"

    def btnNormalStartClick(self):
        print "click"

    def btnEnterLiveRoomStartClick(self):
        print "click"

    def initConfig(self):
        conf = Config("default.ini")
        self.sdkPath = conf.getconf("default").sdk_path  # sdk路径
        self.sdkPathEntry.delete(0, END)
        self.sdkPathEntry.insert(0, self.sdkPath)
        if self.combox.get() == "自动安装":
            self.installMethos = 1
        else:
            self.installMethos = 2

        self.videoPath = ""
        self.firstStartTime = conf.getconf("default").first_start  # 首次启动次数
        self.firstStartEntry.delete(0, END)
        self.firstStartEntry.insert(0, self.firstStartTime)

        self.normaStartTime = conf.getconf("default").normal_start  # 正常启动次数
        self.normalStartEntry.delete(0, END)
        self.normalStartEntry.insert(0, self.normaStartTime)

        self.enterLiveRoonTime = conf.getconf("default").enter_liveroom  # 进入直播间次数
        self.enterLiveRoomEntry.delete(0, END)
        self.enterLiveRoomEntry.insert(0, self.enterLiveRoonTime)

        self.appName = conf.getconf("default").app_name  # app名称
        self.appNameEntry.delete(0, END)
        self.appNameEntry.insert(0, self.appName)

        self.packageName = conf.getconf("default").package  # 包名
        self.packageNameEntry.delete(0, END)
        self.packageNameEntry.insert(0, self.packageName)

        self.appPath = conf.getconf("default").app_path  # 安装包地址
        self.appPathEntry.delete(0, END)
        self.appPathEntry.insert(0, self.appPath)

        self.features = ""  # 特征图
        # self.sdkPathEntry.delete(0, END)
        # self.sdkPathEntry.insert(0, self.sdkPath)

    def createWidgets(self):
        # fm1
        self.fm1 = Frame(self, bg='black')
        self.titleLabel = Label(self.fm1, text="自动化测试脚本", font=('微软雅黑', 24), fg="white", bg='black')
        self.titleLabel.pack()
        self.fm1.pack(side=TOP, expand=YES, fill='y', pady=20)

        # fm2
        self.fm2 = Frame(self, bg='black')
        self.fm2_left = Frame(self.fm2, bg='black')
        self.fm2_right = Frame(self.fm2, bg='black')
        self.fm2_left_top = Frame(self.fm2_left, bg='black')
        self.fm2_left_mid = Frame(self.fm2_left, bg='black')

        self.fm2_left_bottom = Frame(self.fm2_left, bg='black')
        self.fm2_left_bottom1 = Frame(self.fm2_left, bg='black')
        self.fm2_left_bottom2 = Frame(self.fm2_left, bg='black')
        self.fm2_left_bottom3 = Frame(self.fm2_left, bg='black')
        self.fm2_left_bottom4 = Frame(self.fm2_left, bg='black')

        ## --------------------------------------具体属性---------------------------------------------
        self.sdkPathEntry = Entry(self.fm2_left_top, font=('微软雅黑', 10), width='30', fg='#FF4081')
        self.sdkPathBtn = Button(self.fm2_left_top, text='SDK路径', bg='#22C9C9', fg='white',
                                 font=('微软雅黑', 10), width='12', command=self.btnSdkBtnClick)

        self.videoPathEntry = Entry(self.fm2_left_bottom, font=('微软雅黑', 12), width='30', fg='#22C9C9')
        self.videoPathButton = Button(self.fm2_left_bottom, text='上传视频', bg='#22C9C9', fg='white',
                                      font=('微软雅黑', 10), width='12', command=self.btnVideoBtnClick)

        self.packageNameEntry = Entry(self.fm2_left_bottom2, font=('微软雅黑', 12), width='30', fg='#22C9C9')
        self.packageNameButton = Button(self.fm2_left_bottom2, text='测试包名', bg='#22C9C9', fg='white',
                                        font=('微软雅黑', 10), width='12', command=self.btnPackageBtnClick)

        self.appNameEntry = Entry(self.fm2_left_bottom3, font=('微软雅黑', 12), width='30', fg='#22C9C9')
        self.appNameButton = Button(self.fm2_left_bottom3, text='App名称', bg='#22C9C9', fg='white',
                                    font=('微软雅黑', 10), width='12', command=self.btnAppNameClick)

        self.appPathEntry = Entry(self.fm2_left_bottom1, font=('微软雅黑', 12), width='30', fg='#22C9C9')
        self.appPathButton = Button(self.fm2_left_bottom1, text='App路径', bg='#22C9C9', fg='white',
                                    font=('微软雅黑', 10), width='12', command=self.btnAppPathBtnClick)

        self.firstStartEntry = Entry(self.fm2_left_bottom4, font=('微软雅黑', 12), width='5', fg='#22C9C9')
        self.firstStartButton = Button(self.fm2_left_bottom4, text='首次启动次数', bg='#22C9C9', fg='white',
                                       font=('微软雅黑', 10), width='12', command=self.btnfirstStartClick)

        self.normalStartEntry = Entry(self.fm2_left_bottom4, font=('微软雅黑', 12), width='5', fg='#22C9C9')
        self.normalStartButton = Button(self.fm2_left_bottom4, text='非首次启动次数', bg='#22C9C9', fg='white',
                                        font=('微软雅黑', 10), width='12', command=self.btnNormalStartClick)

        self.enterLiveRoomEntry = Entry(self.fm2_left_bottom4, font=('微软雅黑', 12), width='5', fg='#22C9C9')
        self.enterLiveRoomButton = Button(self.fm2_left_bottom4, text='进直播间次数', bg='#22C9C9', fg='white',
                                          font=('微软雅黑', 10), width='12', command=self.btnEnterLiveRoomStartClick)

        self.startModeLabel = Label(self.fm2_left_mid, text='启动方式', bg='#22C9C9', fg='white',
                                    font=('微软雅黑', 10), width='12', )

        # 创建下拉菜单
        self.combox = ttk.Combobox(self.fm2_left_mid)
        self.combox['value'] = ('手动启动', '自动启动')
        self.combox.current(0)
        self.combox.bind("<<ComboboxSelected>>", self.comboxItemListener)

        self.startAppBtn = Button(self.fm2_right, text='启动脚本', bg='black', fg='white',
                                  command=self.startAppBtnClickListener)

        ## ------------------------------------布局-------------------------------------------
        self.fm2.pack(side=TOP, expand=YES, fill="y")
        self.fm2_left.pack(side=TOP, pady=10, fill='x')
        self.fm2_left_top.pack(side=TOP, padx=60, pady=10, expand=YES, fill='x')
        self.fm2_left_mid.pack(side=TOP, padx=60, pady=10, expand=YES, fill='x')
        self.fm2_left_bottom.pack(side=TOP, padx=60, pady=10, expand=YES, fill='x')
        self.fm2_left_bottom1.pack(side=TOP, padx=60, pady=10, expand=YES, fill='x')
        self.fm2_left_bottom2.pack(side=TOP, padx=60, pady=10, expand=YES, fill='x')
        self.fm2_left_bottom3.pack(side=TOP, padx=60, pady=10, expand=YES, fill='x')
        self.fm2_left_bottom4.pack(side=TOP, padx=60, pady=10, expand=YES, fill='x')

        self.startModeLabel.pack(side=LEFT)
        self.combox.pack(side=LEFT, padx=20)
        self.sdkPathBtn.pack(side=LEFT)
        self.sdkPathEntry.pack(side=LEFT, fill='y', padx=20)
        self.videoPathButton.pack(side=LEFT)
        self.videoPathEntry.pack(side=LEFT, fill='y', padx=20)
        self.packageNameButton.pack(side=LEFT)
        self.packageNameEntry.pack(side=LEFT, fill='y', padx=20)
        self.appNameButton.pack(side=LEFT)
        self.appNameEntry.pack(side=LEFT, fill='y', padx=20)
        self.appPathButton.pack(side=LEFT)
        self.appPathEntry.pack(side=LEFT, fill='y', padx=20)
        self.firstStartButton.pack(side=LEFT)
        self.firstStartEntry.pack(side=LEFT, fill='y', padx=20)
        self.normalStartButton.pack(side=LEFT)
        self.normalStartEntry.pack(side=LEFT, fill='y', padx=20)
        self.enterLiveRoomButton.pack(side=LEFT)
        self.enterLiveRoomEntry.pack(side=LEFT, fill='y', padx=20)

        self.fm2_right.pack(side=TOP, pady=10, fill='x')
        self.startAppBtn.pack(side=TOP, expand=YES, fill='y')


if __name__ == '__main__':
    app = Application()
    app.initConfig()
    app.mainloop()
