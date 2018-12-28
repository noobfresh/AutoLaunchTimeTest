# -*- coding: UTF-8 -*-

from calculate.template_match import findLaunchLogo, get_ent_pos

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
    try:
        MLog.debug(u"尝试启动app")
        startAppBySwipe(d, times, video, sernum, machineName)
    except Exception, e:
        MLog.debug(u"startAPP:" + u"启动app失败! e = " + repr(e) + "  " + machineName)
        sysExit(u"程序退出,原因:启动app失败!")


def startAppBySwipe(d, times, video, sernum, machineName):
    conf = Config("default.ini")
    app_name = conf.getconf("default").app_name

    screenRecord(d, times, video, sernum, machineName)
    try:
        MLog.info("startAppBySwipe:" + u"try start app ,name = " + app_name)
        d(text=app_name).click()
    except Exception, e:
        MLog.info(repr(e))
        app_name = "@" + app_name
        MLog.info(u"start_app startAppBySwipe: change app's start name , appname is " + app_name)
        d(text=app_name).click()


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
    img_name = sernum + "_cap.png"
    cmd1 = r"adb -s " + sernum + " shell /system/bin/screencap -p /sdcard/" + img_name
    cmd2 = r"adb -s " + sernum + " pull /sdcard/" + img_name + " " + out_path + img_name
    checkSrcVialdAndAutoCreate('./cap/')
    os.system(cmd1)
    os.system(cmd2)
    print 'cap ====1'
    return out_path + img_name


def enter(d, times, video, sernum, machineName, package):
    path = cap(sernum)
    x, y = get_ent_pos(path)
    screenRecord(d, times, video, sernum, machineName)
    time.sleep(2)
    print 'enter before click'
    d.click(x, y)
    print 'enter after click'
    time.sleep(6)
    if package == 'com.duowan.mobile':
        print 'shou yy'
        d(resourceId="com.duowan.mobile.entlive:id/btn_exit_portrait").click()
    elif package == 'sg.bigo.live':
        print 'bigo live'
        d(resourceId="sg.bigo.live:id/btn_live_video_close").click()


if __name__ == '__main__':
    sernum = 'b2dcaa55'
    out_path = os.path.dirname(__file__) + os.sep + "cap" + os.sep
    img_name = sernum + "_cap.jpg"
    cmd1 = r"adb -s " + sernum + " shell /system/bin/screencap -p /sdcard/" + img_name
    cmd2 = r"adb -s " + sernum + " pull /sdcard/" + img_name + " " + out_path + img_name
    checkSrcVialdAndAutoCreate('./cap/')
    os.system(cmd1)
    os.system(cmd2)
