# -*- coding: UTF-8 -*-

import os
import shutil
import re

save_dir = '/sdcard/screenrecord/'


# 创建文件夹
def mkdir(name, sernum):
    os.system('adb -s ' + sernum + ' shell rm -rf ' + save_dir + name)
    os.system('adb -s' + sernum + ' shell mkdir -p ' + save_dir + name)
    print u'SD卡文件夹创建成功'
    path = os.path.dirname(__file__) + "\\"
    os.chdir(path)
    print u'创建文件夹' + path
    if os.path.exists(name):
        shutil.rmtree(name)
    print name
    os.makedirs(name)
    print u'PC文件夹创建成功'


# Windows文件名检查
def checkNameValid(name=None):
    if name is None:
        print("name is None!")
        return
    reg = re.compile(r'[\\/:*?"<>|\s\r\n]+')
    valid_name = reg.findall(name)
    if valid_name:
        for nv in valid_name:
            name = name.replace(nv, "")
    return name


def removeDirs(dir, sernum):
    os.system('adb  -s ' + sernum + ' shell rm -rf ' + dir)
