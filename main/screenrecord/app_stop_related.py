# -*- coding: UTF-8 -*-

from config.configs import Config
import os

conf = Config("default.ini")
packageName = conf.getconf("default").package


# 安装应用
def installAPK(name):
    path = os.path.dirname(__file__) + "\\"
    os.chdir(path)
    print path
    os.system("adb install " + name)
    print u'安装成功'


# 杀进程
def killProcess():
    os.system('adb shell am force-stop ' + packageName)
    print '---kill process ---'


# 清除数据
def clearData():
    os.system('adb shell pm clear ' + packageName)
    print u'清除数据'


# 卸载应用
def uninstallAPK():
    os.system('adb uninstall ' + packageName)
