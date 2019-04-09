# -*- coding: UTF-8 -*-

from screenrecord.BaseConfig import BaseConfig
import os

from screenrecord.FileOperation import FileOperation


class DeviceInfo(BaseConfig):

    def __init__(self, serialnum):
        super(DeviceInfo, self).__init__()
        self.fileOperation = FileOperation(serialnum)
        self.serialNum = serialnum

    def getDeviceInfo(self):
        deviceName = os.popen('adb -s  ' + self.serialNum + ' shell getprop ro.product.model').read()
        validName = self.fileOperation.checkNameValid(deviceName)
        return validName
