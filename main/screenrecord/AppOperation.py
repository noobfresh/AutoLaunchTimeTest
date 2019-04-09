# -*- coding: UTF-8 -*-

from screenrecord.BaseConfig import BaseConfig
import os

from log.log import MLog
from uitl.baseUtil import sysExit
from uitl.fileUtil import fileExist


class AppOperation(BaseConfig):

    def __init__(self, sernum, params):
        super(AppOperation, self).__init__()
        self.serNum = sernum
        self.param = params
        pass

    # 安装应用
    def installAPK(self, name):
        feature_path = self.getFeaturePath()
        path = os.path.dirname(__file__) + "\\"
        os.chdir(path)
        print path
        apk_path = feature_path + os.sep + "apk" + os.sep + name
        if not fileExist(apk_path):
            MLog.error(u"installAPK:" + u"请检查下你的apk安装包 " + name + u" 是否放置在:" + feature_path + u"中的apk分类的路径下!")
            sysExit(u"应用退出,原因:安装失败!")
        MLog.debug(u"installAPK: 执行安装操作，包路径apk_path = " + apk_path)
        os.system("adb -s " + self.serNum + " install " + apk_path)
        MLog.info(u"app_operation installAPK: 安装成功! sermun = " + self.serNum)

    # 杀进程
    def killProcess(self):
        MLog.info(u"app_operation killProcess: 执行杀进程 ，sernum = " + self.serNum)
        os.system('adb -s ' + self.serNum + ' shell am force-stop ' + self.getPackage())

    # 清除数据
    def clearData(self):
        MLog.info(u"app_operation clearData: 执行清除数据，sernum = " + self.serNum)
        os.system('adb -s ' + self.serNum + ' shell pm clear ' + self.getPackage())

    # 卸载应用
    def uninstallAPK(self):
        MLog.info(u"app_operation uninstallAPK: 执行卸载应用，sernum =" + self.serNum)
        os.system('adb -s ' + self.serNum + '  uninstall ' + self.getPackage())
