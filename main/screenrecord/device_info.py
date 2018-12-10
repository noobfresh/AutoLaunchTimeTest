# -*- coding: UTF-8 -*-

import os
import re
from file_related import checkNameValid


# 拿设备信息防止文件夹重名
def getDeviceInfo(serialnum):
    deviceName = os.popen('adb -s  ' + serialnum + ' shell getprop ro.product.model').read()
    deviceName = re.sub('\s', '', deviceName)
    validName = checkNameValid(deviceName)
    print "machine name = {}".format(deviceName)
    return validName
