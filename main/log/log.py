# coding:utf-8
import logging
import os
import time


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

        print "日志地址: " + self.log_name
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

    def info(self, content):
        self.logger.info(content)

    def error(self, content):
        self.logger.error(content)

    def warn(self, content):
        self.logger.warn(content)


MLog = Log()

if __name__ == '__main__':
    MLog.debug("test")
