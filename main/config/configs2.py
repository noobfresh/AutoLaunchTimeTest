# coding:utf-8
import codecs
import os
import ConfigParser

from log.log import MLog


class Config2(object):
    """
    ConfigParser二次封装，在字典中获取value
    """

    def __init__(self, file_name):
        # 设置conf.ini路径
        self.config_name = file_name
        current_dir = os.path.dirname(__file__)
        top_one_dir = os.path.dirname(current_dir)
        file_name = top_one_dir + os.sep + "config" + os.sep + "files" + os.sep + file_name
        self.file_name = file_name

        self.config = ConfigParser.ConfigParser()
        self.config.readfp(codecs.open(file_name, "r", "utf-8-sig"))

    def get(self, section, option, default=""):
        """
        用法：
        conf = Config()
        info = conf.get("main","url)
        """
        if section in self.config.sections():
            pass
        else:
            MLog.info(u"configs2 get: " + u"配置文件中找不到该 section :" + str(section) + u"直接返回空字符串")
            return default
        return self.config.get(section, option)

    def add(self, section, option, value):
        if section not in self.config._sections:
            self.config.add_section(section)
        self.config.set(section, option, value)

        with open(self.file_name, "w+") as f:
            self.config.write(f)

    def update(self, section, option, value):
        self.add(section, option, value)

    def delete(self, section, option):
        self.config.read(self.config_name)
        self.config.remove_option(section, option)
        # self.config.remove_section(section)
        # write to file
        with open(self.file_name, "w+") as f:
            self.config.write(f)

    def deleteAll(self, section, ):
        self.config.read(self.config_name)
        self.config.remove_section(section)
        # write to file
        with open(self.file_name, "w+") as f:
            self.config.write(f)


if __name__ == "__main__":
    conf = Config2("test.ini")
    info = conf.get("yy", "name")
    # conf.add("moni", "yy", "test23")
    # conf.delete("moni", "yy")
    # conf.deleteAll("moni")
    print info
