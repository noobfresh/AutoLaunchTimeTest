# -*- coding: UTF-8 -*-

from calculate.template_match import findLaunchLogo

from log.log import MLog
import settings
import time
from config.configs import Config
import os
from device_info import getDeviceInfo
from uitl.baseUtil import sysExit
from uitl.fileUtil import checkSrcVialdAndAutoCreate
from video_operation import screenRecord

conf = Config("default.ini")
path = conf.getconf("default").feature_path


# 启动应用
def startAPP(d, times, video, sernum, machineName):
    # os.system('adb shell monkey -p '+packageName+' -c android.intent.category.LAUNCHER 1')
    try:
        MLog.debug(u"尝试启动app")
        startAppBySwipe(d, times, video, sernum, machineName)
    except Exception, e:
        MLog.debug(u"startAPP:" + u"启动app失败! e = " + repr(e) + "  " + machineName)
        sysExit(u"程序退出,原因:启动app失败!")


def startAppBySwipe(d, times, video, sernum, machineName):
    conf = Config("default.ini")
    app_name = conf.getconf("default").app_name

    try:
        MLog.info("startAppBySwipe:" + u"try start app ,name = " + app_name)

        pos = settings.get_value(sernum + "pos", None)
        if pos is None:
            MLog.info(u"start_app startAppBySwipe: get pos from setting is None! so get pos from function getPos().")
            pos = getPos(d, app_name, sernum)
    except Exception, e:
        MLog.info(repr(e))
        app_name = "@" + app_name
        MLog.info(u"start_app startAppBySwipe: change app's start name , appname is " + app_name)
        # d(text=app_name).click()
        pos = getPos(d, app_name, sernum)

    MLog.debug("startAppBySwipe:" + str(pos))
    # offset代表偏移量，方便点中logo中间部分
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
    MLog.info(u"start_app getPos: appname = " + app_name + u" sernum = " + sernum)
    machineName = getDeviceInfo(sernum)
    conf = Config("apk.ini")
    conf_default = Config("default.ini")
    app_key = conf_default.getconf("default").app
    feature_dir = conf.getconf(str(app_key)).feature

    if machineName == "vivoX9" or machineName == "vivoX7":
        img_path = path + "/picrepos/feature/" + feature_dir + "/" + machineName + "_start_feature.jpg"
        MLog.info(u"start_app getPos: img_path = " + img_path)
        pos = findLaunchLogo(cap(sernum), img_path)
    else:
        MLog.debug("get pos by uiautomator")
        pos = d(text=app_name).bounds
    settings.set_value(sernum + "pos", pos)
    return pos


def cap(sernum):
    out_path = os.path.dirname(__file__) + os.sep + "cap" + os.sep
    img_name = sernum + "_cap.jpg"
    cmd1 = r"adb -s " + sernum + " shell /system/bin/screencap -p /sdcard/" + img_name
    cmd2 = r"adb -s " + sernum + " pull /sdcard/" + img_name + " " + out_path + img_name
    checkSrcVialdAndAutoCreate('./cap/')
    os.system(cmd1)
    os.system(cmd2)

    return out_path + img_name


if __name__ == '__main__':
    sernum = 'b2dcaa55'
    out_path = os.path.dirname(__file__) + os.sep + "cap" + os.sep
    img_name = sernum + "_cap.jpg"
    cmd1 = r"adb -s " + sernum + " shell /system/bin/screencap -p /sdcard/" + img_name
    cmd2 = r"adb -s " + sernum + " pull /sdcard/" + img_name + " " + out_path + img_name
    checkSrcVialdAndAutoCreate('./cap/')
    os.system(cmd1)
    os.system(cmd2)
