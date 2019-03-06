# -*- coding: UTF-8 -*-
from screenrecord.BaseConfig import BaseConfig
from calculate.template_match import get_ent_pos
from log.log import MLog
import time
from config.configs import Config
import os
from screenrecord.DeviceInfo import DeviceInfo
from screenrecord.VideoOperation import VideoOperation
from uitl.baseUtil import sysExit
from uitl.fileUtil import checkSrcVialdAndAutoCreate


class StartApp(BaseConfig):
    def __init__(self, sernum):
        super(StartApp, self).__init__()
        self.serNum = sernum
        self.device = DeviceInfo(sernum)
        self.machineName = self.device.getDeviceInfo()
        self.videoOperation = VideoOperation(sernum)

    # 启动应用
    def startAPP(self, d, times, video):
        try:
            MLog.debug(u"尝试启动app")
            self.startAppBySwipe(d, times, video)
        except Exception, e:
            MLog.debug(u"startAPP:" + u"启动app失败! e = " + repr(e) + "  " + self.machineName)
            sysExit(u"程序退出,原因:启动app失败!")

    def startAppBySwipe(self, d, times, video):
        conf = Config("default.ini")
        app_name = conf.getconf("default").app_name
        try:
            MLog.info("startAppBySwipe:" + u"try start app ,name = " + app_name)
            bounds = d(text=app_name).info['bounds']
            print bounds
        except Exception, e:
            MLog.info(repr(e))
            app_name = "@" + app_name
            MLog.info(u"start_app startAppBySwipe: change app's start name , appname is " + app_name)
        self.videoOperation.screenRecord(d, times, video)
        MLog.info(u"start_app startAppBySwipe: click app logo.")
        d(text=app_name).click()

    def cap(self):
        out_path = os.path.dirname(__file__) + os.sep + "cap" + os.sep
        img_name = self.serNum + "_cap.png"
        cmd1 = r"adb -s " + self.serNum + " shell /system/bin/screencap -p /sdcard/" + img_name
        cmd2 = r"adb -s " + self.serNum + " pull /sdcard/" + img_name + " " + out_path + img_name
        checkSrcVialdAndAutoCreate('./cap/')
        os.system(cmd1)
        os.system(cmd2)
        print 'cap ====1'
        return out_path + img_name, out_path

    # 进入直播间
    def enter(self, d, times, video, package):
        path, out_path = self.cap()
        x, y = get_ent_pos(path, out_path, self.machineName)
        self.videoOperation.screenRecord(d, times, video)
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
