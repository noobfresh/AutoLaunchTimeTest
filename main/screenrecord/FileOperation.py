# -*- coding: UTF-8 -*-
from screenrecord.BaseConfig import BaseConfig
import os
import shutil
import re

from log.log import MLog


class FileOperation(BaseConfig):

    def __init__(self, sernum):
        super(FileOperation, self).__init__()
        self.saveDir = '/sdcard/screenrecord/'
        self.serNum = sernum

    # 创建文件夹
    def mkdir(self, name):
        os.system('adb -s ' + self.serNum + ' shell rm -rf ' + self.saveDir + name)
        os.system('adb -s ' + self.serNum + ' shell mkdir -p ' + self.saveDir + name)
        MLog.debug(u"file_operation mkdir: SD卡文件夹创建成功")
        path = os.path.dirname(__file__) + "\\"
        os.chdir(path)
        MLog.debug(u"file_operation mkdir:" + u'创建文件夹' + path)
        if os.path.exists(name):
            shutil.rmtree(name)
        print name
        os.makedirs(name)
        MLog.debug(u"file_operation mkdir: 'PC文件夹创建成功")

    # Windows文件名检查
    def checkNameValid(self, name=None):
        if name is None:
            print("name is None!")
            return
        reg = re.compile(r'[\\/:*?"<>|\s\r\n]+')
        valid_name = reg.findall(name)
        if valid_name:
            for nv in valid_name:
                name = name.replace(nv, "")
        return name

    def removeDirs(self, dir):
        os.system('adb  -s ' + self.serNum + ' shell rm -rf ' + dir)
