# coding:utf-8
import codecs
import os
import ConfigParser


class Dictionary(dict):
    """
    把config.ini中的参数添加值dict
    """

    def __getattr__(self, keyname):
        # 如果key值不存在则返回默认值"not find config keyname"
        return self.get(keyname, "config.ini中没有找到对应的keyname")


class Config(object):
    """
    ConfigParser二次封装，在字典中获取value
    """

    def __init__(self, file_name):
        # 设置conf.ini路径
        current_dir = os.path.dirname(__file__)
        top_one_dir = os.path.dirname(current_dir)
        file_name = top_one_dir + os.sep + "config" + os.sep + "files" + os.sep + file_name
        # 实例化ConfigParser对象
        # self.config = ConfigParser.ConfigParser()
        # self.config.read(file_name)
        self.config = ConfigParser.ConfigParser()
        self.config.readfp(codecs.open(file_name, "r", "utf-8-sig"))
        # 根据section把key、value写入字典
        for section in self.config.sections():
            setattr(self, section, Dictionary())
            for keyname, value in self.config.items(section):
                setattr(getattr(self, section), keyname, value)

    def getconf(self, section):
        """
        用法：
        conf = Config()
        info = conf.getconf("main").url
        """
        if section in self.config.sections():
            pass
        else:
            print ("配置文件中找不到该 section :" + str(section))

        return getattr(self, section)


if __name__ == "__main__":
    conf = Config("apk.ini")
    info = conf.getconf("yy").name
    print info
