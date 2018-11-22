# coding:utf-8
import os
import ConfigParser


class Dictionary(dict):
    '''
    把config.ini中的参数添加值dict
    '''

    def __getattr__(self, keyname):
        # 如果key值不存在则返回默认值"not find config keyname"
        return self.get(keyname, "config.ini中没有找到对应的keyname")


class Config(object):
    '''
    ConfigParser二次封装，在字典中获取value
    '''

    def __init__(self):
        # 设置conf.ini路径
        current_dir = os.path.dirname(__file__)
        top_one_dir = os.path.dirname(current_dir)
        file_name = top_one_dir + "\\config\\default.init"
        # 实例化ConfigParser对象
        self.config = ConfigParser.ConfigParser()
        self.config.read(file_name)
        # 根据section把key、value写入字典
        for section in self.config.sections():
            setattr(self, section, Dictionary())
            for keyname, value in self.config.items(section):
                setattr(getattr(self, section), keyname, value)

    def getconf(self, section):
        '''
        用法：
        conf = Config()
        info = conf.getconf("main").url
        '''
        if section in self.config.sections():
            pass
        else:
            print("config.ini 找不到该 section")
        return getattr(self, section)

    def getdefaultconf(self):
        '''
        用法：
        conf = Config()
        info = conf.getconf("main").url
        '''

        print "使用默认的section : 'default'"
        section = 'default'
        if section in self.config.sections():
            pass
        else:
            print("config.ini 找不到该 section")
        return getattr(self, section)

# if __name__ == "__main__":

# conf = Config()
# info = conf.getconf("default").frame
# print info
