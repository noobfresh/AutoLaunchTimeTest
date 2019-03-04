# coding=utf-8
import ttk
from Tkinter import Frame, YES, BOTH, Label, TOP, Entry, LEFT, Button

from main import start


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

    def doSomething(self):
        print 'sdk = ' + self.sdkPathEntry.get()
        print 'video = ' + self.videoPathEntry.get()

    def startApp(self):
        print 'sdk = ' + self.sdkPathEntry.get()
        start()

    def clickListener(self, event):
        print self.combox.get()

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
        self.sdkPathLabel = Label(self.fm2_left_top, text='SDK路径', bg='#22C9C9', fg='white',
                                  font=('微软雅黑', 10), width='16', )

        self.videoPathEntry = Entry(self.fm2_left_bottom, font=('微软雅黑', 12), width='30', fg='#22C9C9')
        self.videoPathLabel = Label(self.fm2_left_bottom, text='上传视频', bg='#22C9C9', fg='white',
                                    font=('微软雅黑', 10), width='16', )

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
        self.sdkPathLabel.pack(side=LEFT)
        self.sdkPathEntry.pack(side=LEFT, fill='y', padx=20)
        self.videoPathLabel.pack(side=LEFT)
        self.videoPathEntry.pack(side=LEFT, fill='y', padx=20)

        self.fm2_right.pack(side=TOP, pady=10, fill='x')
        self.startAppBtn.pack(side=TOP, expand=YES, fill='y')


if __name__ == '__main__':
    app = Application()
    # to do
    app.mainloop()
