# -*- coding: UTF-8 -*-
import settings
from multiprocessing import Pool
import subprocess

from screenrecord.BusinessEntrance import BusinessEntrance

serial = []


def getDevices():
    devices = subprocess.Popen('adb devices'.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    for item in devices.split():
        filters = ['list', 'of', 'device', 'devices', 'attached']
        if item.lower() not in filters:
            serial.append(item)
    return serial


def enterMethodDelegate(methodDelegatedObject):
    return methodDelegatedObject.screenmain()


def start_python( serial_num, params):
    bussinessEntarnce = BusinessEntrance(serial_num, params)
    # 加上下面两行
    settings._init()
    settings.set_value("ffmpeg", 30)
    bussinessEntarnce.screenmain()


if __name__ == "__main__":
    getDevices()
    # p = Pool(5)
    for index in range(len(serial)):
        serNum = serial[index]
        bussinessEntarnce = BusinessEntrance(serNum, 1)
        # 加上下面两行
        settings._init()
        settings.set_value("ffmpeg", 30)
        bussinessEntarnce.screenmain()
    #     result = p.apply_async(enterMethodDelegate, args=(bussinessEntarnce,))
    #     result.get()
    # p.close()
    # p.join()
