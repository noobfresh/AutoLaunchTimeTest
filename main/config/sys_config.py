# -*- coding: UTF-8 -*-
import re

from config.configs import Config
from log.log import MLog
from screenrecord.device_info import getDeviceInfo


def get_device_params():
    conf = Config("default.ini")
    event = conf.getconf("serial").serial_number
    serial = event.split(',')
    device_name = getDeviceInfo(serial[0])  # device name 看看韦总到时候怎么处理，把这一个干掉，我这边的操作其实很多余
    device_name = re.sub('\s', '', device_name)
    return device_name


def getApkName():
    conf = Config("default.ini")
    apkName = conf.getconf("default").apk_name
    return apkName


def get_start_params():
    frame = 30
    firstLaunchTimes = 1
    notFirstLaunchTimes = 1
    apkName = u"yy.apk"

    try:
        print u"使用配置文件参数..."
        conf = Config("default.ini")
        frame = conf.getconf("default").frame
        firstLaunchTimes = conf.getconf("default").first_start
        notFirstLaunchTimes = conf.getconf("default").normal_start
        apkName = conf.getconf("default").apk_name

    except Exception:
        MLog.error(u"获取参数错误,使用默认值")
        frame = 30
        firstLaunchTimes = 1
        notFirstLaunchTimes = 1
        apkName = u"yy.apk"
    finally:
        # start_python 需要运行在init_ffmpeg后面，否则拿不到帧数的值
        MLog.info("apk = " + str(apkName) + " ,first_start = " \
                  + str(firstLaunchTimes) + " ,normal_start = " + str(notFirstLaunchTimes) + " ,frame = " + str(frame))

    return int(firstLaunchTimes), int(notFirstLaunchTimes), str(apkName)
