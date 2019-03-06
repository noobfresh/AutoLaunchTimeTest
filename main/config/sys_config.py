# -*- coding: UTF-8 -*-
import re

from config.configs import Config
from log.log import MLog
from screenrecord.DeviceInfo import DeviceInfo


def get_device_params():
    conf = Config("default.ini")
    event = conf.getconf("serial").serial_number
    serial = event.split(',')
    deviceInfo = DeviceInfo(serial[0])
    device_name = deviceInfo.getDeviceInfo()  # device name 看看韦总到时候怎么处理，把这一个干掉，我这边的操作其实很多余
    device_name = re.sub('\s', '', device_name)
    return device_name


def getApkName():
    conf = Config("default.ini")
    apkName = conf.getconf("default").apk_name
    return apkName


def get_start_params():
    frame = 50
    firstLaunchTimes = 0
    notFirstLaunchTimes = 0
    enterLiveTimes = 1
    apkName = u"yy.apk"
    package = u"com.duowan.mobile"

    try:
        MLog.info(u"sys_config get_start_params: 读取配置文件参数...")
        conf = Config("default.ini")
        frame = conf.getconf("default").frame
        firstLaunchTimes = conf.getconf("default").first_start
        notFirstLaunchTimes = conf.getconf("default").normal_start
        enterLiveTimes = conf.getconf("default").enter_liveroom
        apkName = conf.getconf("default").apk_name
        package = conf.getconf("default").package

    except Exception:
        MLog.error(u"获取参数错误,使用默认值")
        frame = 50
        firstLaunchTimes = 1
        notFirstLaunchTimes = 1
        enterLiveTimes = 1
        apkName = u"yy.apk"
        package = u"com.duowan.mobile"
    finally:
        # start_python 需要运行在init_ffmpeg后面，否则拿不到帧数的值
        MLog.info("apkName = " + str(apkName) + " ,first_start = " \
                  + str(firstLaunchTimes) + " ,normal_start = " + str(notFirstLaunchTimes) + " ,frame = " + str(frame))

    return int(firstLaunchTimes), int(notFirstLaunchTimes), int(enterLiveTimes), str(apkName), str(package)
