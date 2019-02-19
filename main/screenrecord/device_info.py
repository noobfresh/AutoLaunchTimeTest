# -*- coding: UTF-8 -*-

import os

from file_operation import checkNameValid


# 拿设备信息防止文件夹重名
from log.log import MLog


def getDeviceInfo(serialnum):
    deviceName = os.popen('adb -s  ' + serialnum + ' shell getprop ro.product.model').read()
    validName = checkNameValid(deviceName)
    return validName
