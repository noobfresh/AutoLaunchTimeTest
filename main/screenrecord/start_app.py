# -*- coding: UTF-8 -*-

from calculate.template_match import findLaunchLogo
from screenrecord.screencap import cap
import sys
from log.log import MLog
import settings
import time
from config.configs import Config
import os
from device_info import getDeviceInfo
from uitl.baseUtil import sysExit
from video_related import screenRecord

conf = Config("default.ini")
path = conf.getconf("default").feature_path


# 启动应用
def startAPP(d, times, video, sernum, machineName):
    # os.system('adb shell monkey -p '+packageName+' -c android.intent.category.LAUNCHER 1')
    try:
        MLog.debug(u"尝试启动app")
        startAppBySwipe(d, times, video, sernum, machineName)
    except Exception, e:
        MLog.debug(u"startAPP:" + u"启动app失败! e = " + repr(e))
        sysExit(u"程序退出,原因:启动app失败!")


def startAppBySwipe(d, times, video, sernum, machineName):
    conf = Config("default.ini")
    app_name = conf.getconf("default").app_name

    try:
        MLog.info("startAppBySwipe:" + u"try start app ,name = " + app_name)
        pos = settings.get_value("pos", None)
        if pos is None:
            pos = getPos(d, app_name, sernum)
    except Exception, e:
        MLog.info(repr(e))
        app_name = "@" + app_name
        pos = getPos(d, app_name, sernum)

    MLog.debug("startAppBySwipe:" + str(pos))
    # offset代表偏移量，方便点中logo中间部分
    startTime = time.time()
    screenRecord(d, times, video, sernum, machineName)
    time.sleep(2)
    offset = 0
    left = pos['left'] + offset
    top = pos['top'] + offset
    right = pos['right']
    bottom = pos['bottom']

    x = (left + right) >> 1
    y = (top + bottom) >> 1
    duration = 10
    start_shell = "adb -s " + sernum + "  shell input swipe " + str(x) + " " + str(y) + " " + str(x + 1) + " " + str(
        y) + " " + str(
        duration)
    MLog.info(start_shell)
    os.system(start_shell)


# 某些特定手机点不到，通过图片匹配去点击
def getPos(d, app_name, sernum):
    machineName = getDeviceInfo(sernum)
    conf = Config("apk.ini")
    conf_default = Config("default.ini")
    app_key = conf_default.getconf("default").app
    feature_dir = conf.getconf(str(app_key)).feature
    if machineName == "vivoX9":
        MLog.info("get pos by cap findLaunchLogo")
        pos = findLaunchLogo(cap(), path + "/picrepos/feature/" + feature_dir + "/vivoX9_launch_feature.jpg")
    elif machineName == "vivoX7":
        MLog.info("get pos by cap findLaunchLogo")
        pos = findLaunchLogo(cap(), path + "/picrepos/feature/" + feature_dir + "/vivoX7_launch_feature.jpg")
    else:
        MLog.debug("get pos by uiautomator")
        pos = d(text=app_name).bounds
    settings.set_value("pos", pos)
    return pos
