# -*- coding: UTF-8 -*-

from config.configs import Config
import os

from log.log import MLog
from uitl.baseUtil import sysExit
from uitl.fileUtil import fileExist

conf = Config("default.ini")
packageName = conf.getconf("default").package
feature_path = conf.getconf("default").feature_path


# 安装应用
def installAPK(name, sermun):
    path = os.path.dirname(__file__) + "\\"
    os.chdir(path)
    print path
    # TODO 等后面让韦镒帮忙看看路径切换是否需要干掉，先指定目录
    apk_path = feature_path + os.sep + "apk" + os.sep + name
    if not fileExist(apk_path):
        MLog.error(u"installAPK:" + u"请检查下你的apk安装包 " + name + u" 是否放置在:" + feature_path + u"中的apk分类的路径下!")
        sysExit(u"应用退出,原因:安装失败!")
    MLog.debug(u"installAPK: apk_path = " + apk_path)
    os.system("adb -s " + sermun + " install " + apk_path)
    print u'安装成功'


# 杀进程
def killProcess(sernum):
    os.system('adb -s ' + sernum + ' shell am force-stop ' + packageName)
    print '---kill process ---'


# 清除数据
def clearData(sernum):
    os.system('adb -s ' + sernum + ' shell pm clear ' + packageName)
    print u'清除数据'


# 卸载应用
def uninstallAPK(sernum):
    os.system('adb -s ' + sernum + '  uninstall ' + packageName)
