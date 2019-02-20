# coding:utf-8
import ctypes
import logging
import os
import time

FOREGROUND_BLUE = 0x0001  # text color contains blue.
FOREGROUND_GREEN = 0x0002  # text color contains green.
FOREGROUND_RED = 0x0004  # text color contains red.
FOREGROUND_INTENSITY = 0x0008  # text color is intensified.
FOREGROUND_WHITE = FOREGROUND_BLUE | FOREGROUND_GREEN | FOREGROUND_RED
# winbase.h
STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

# wincon.h
FOREGROUND_BLACK = 0x0000
FOREGROUND_BLUE = 0x0001
FOREGROUND_GREEN = 0x0002
FOREGROUND_CYAN = 0x0003
FOREGROUND_RED = 0x0004
FOREGROUND_MAGENTA = 0x0005
FOREGROUND_YELLOW = 0x0006
FOREGROUND_GREY = 0x0007
FOREGROUND_INTENSITY = 0x0008  # foreground color is intensified.

BACKGROUND_BLACK = 0x0000
BACKGROUND_BLUE = 0x0010
BACKGROUND_GREEN = 0x0020
BACKGROUND_CYAN = 0x0030
BACKGROUND_RED = 0x0040
BACKGROUND_MAGENTA = 0x0050
BACKGROUND_YELLOW = 0x0060
BACKGROUND_GREY = 0x0070
BACKGROUND_INTENSITY = 0x0080  # background color is intensified.

STD_OUTPUT_HANDLE = -11
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


def set_color(color, handle=std_out_handle):
    bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return bool


class Log(object):
    """
        封装后的logging
    """

    def __new__(cls):
        # 关键在于这，每一次实例化的时候，我们都只会返回这同一个instance对象
        if not hasattr(cls, 'instance'):
            cls.MLog = super(Log, cls).__new__(cls)
        return cls.MLog

    def __init__(self):
        """
            指定保存日志的文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        """
        logger = "MLog"
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        # 创建一个handler，用于写入日志文件

        self.suffix = '.txt'
        self.log_time = time.strftime("%Y_%m_%d_%H_%M")
        self.log_path = os.path.dirname(__file__) + os.sep + "files" + os.sep
        self.log_name = self.log_path + "log_" + self.log_time + self.suffix

        if not os.path.exists(self.log_path):
            print u"文件路径不存在，现在创建一个..."
            print self.log_path
            os.mkdir(self.log_path)

        # print u"日志地址: " + self.log_name
        fh = logging.FileHandler(self.log_name, 'a')  # 追加模式  这个是python2的
        # fh = logging.FileHandler(self.log_name, 'a', encoding='utf-8')  # 这个是python3的
        fh.setLevel(logging.DEBUG)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 定义handler的输出格式
        formatter = logging.Formatter(
            '[%(asctime)s] %(filename)s->%(funcName)s line:%(lineno)d [%(levelname)s]%(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        #  添加下面一句，在记录日志之后移除句柄
        # self.logger.removeHandler(ch)
        # self.logger.removeHandler(fh)
        # 关闭打开的文件
        fh.close()
        ch.close()

    def debug(self, content):
        self.logger.debug(content)

    def info(self, content, color=FOREGROUND_GREEN):
        set_color(color)
        self.logger.info(content)
        set_color(FOREGROUND_WHITE)

    def warn(self, content, color=FOREGROUND_YELLOW):
        set_color(color)
        self.logger.warn(content)
        set_color(FOREGROUND_WHITE)

    def error(self, content, color=FOREGROUND_RED):
        set_color(FOREGROUND_RED)
        self.logger.error(content)
        set_color(FOREGROUND_WHITE)


MLog = Log()

if __name__ == '__main__':
    MLog.debug("test")
    MLog.info(u"log :" + "test")
    MLog.warn(u"log :" + "test")
    MLog.error(u"log :" + "error")
    name = raw_input()
