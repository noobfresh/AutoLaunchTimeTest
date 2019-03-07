# -*- coding: UTF-8 -*-
import shutil
import time

from log.log import MLog
from screenrecord.AppOperation import AppOperation
from screenrecord.BaseConfig import BaseConfig
from screenrecord.DeviceInfo import DeviceInfo
import os
import settings
import uiautomator2 as u2

# 解决即使把adb加入到了path，python也调不到的问题（为了使用UIAutomator引入的）
from screenrecord.FileOperation import FileOperation
from screenrecord.RegisterEvent import RegisterEvent
from screenrecord.StartApp import StartApp
from screenrecord.SubThread import doInThread
from screenrecord.VideoOperation import VideoOperation

os.environ.__delitem__('ANDROID_HOME')
os.environ.__setitem__('ANDROID_HOME', 'C:/Android/')
os.environ.update()


class BusinessEntrance(BaseConfig):

    def __init__(self, sernum, params):
        super(BusinessEntrance, self).__init__()
        self.param = params
        self.serNum = sernum
        self.method = params.install_method
        self.device = DeviceInfo(sernum)
        self.tempDir = self.device.getDeviceInfo()
        self.serial = []
        self.d = u2.connect(sernum)
        self.registerEvent = RegisterEvent(sernum)
        self.appOperation = AppOperation(sernum, params)
        self.fileOperation = FileOperation(sernum)
        self.videoOperation = VideoOperation(sernum)
        self.machineName = self.tempDir
        self.startApp = StartApp(sernum)

    def start_python(self):
        MLog.info(u"screen_record_main start_python: serial_num = " + str(self.serNum))
        self.screenmain()

    # main函数，线程sleep时间有待商榷
    def screenmain(self):

        MLog.info(u"screen_record_main screenmain: sernum = " + str(self.serNum))
        MLog.info(u"screen_record_main screenmain: "
                  + " firstLaunchTimes = " + str(self.getFirstStartTime())
                  + " notFirstLaunchTimes = " + str(self.getNormalStartTime())
                  + " apkName = " + self.getApkName())
        settings._init()
        try:
            d = u2.connect(self.serNum)
            doInThread(self.registerEvent.runwatch, d, 0)
            time.sleep(10)
            doInThread(self.registerEvent.inputListener, d, 0, self.serNum)
            time.sleep(20)

            if self.method == 1:  # 自动安装
                self.firstLaunch()
            elif self.method == 2:  # 手动安装
                self.firstLaunch2()

            self.notFirstLaunch()
            self.enterLiveRoom()
        except BaseException, e:
            MLog.error("BaseException = " + repr(e))

    # 首次启动
    def firstLaunch(self):
        if self.getFirstStartTime() > 0:
            if self.machineName == "PACM00":
                self.fileOperation.removeDirs("/sdcard/DCIM/Screenshots")
                MLog.info(u"删除 screenshot")
                path = os.path.dirname(__file__) + "\\"
                MLog.debug(u"screen_record_main firstLaunch: path = " + path)
                os.chdir(path)
                if os.path.exists("Screenshots"):
                    shutil.rmtree("Screenshots")
            self.appOperation.uninstallAPK()

            # firstTimes = firstLaunchTimes * 20
            first_dir = self.tempDir + "_first"
            self.fileOperation.mkdir(first_dir)
            if self.machineName != "PACM00":
                self.appOperation.installAPK(self.getApkName())
                time.sleep(20)  # 后续改成轮询是否有安装包的包名，有再录屏
            # screenRecord(firstTimes, first_dir + '/' + 'first.mp4')
            # startTime = time.time()
            for index in range(int(self.getFirstStartTime())):
                if self.machineName == "PACM00":
                    self.appOperation.uninstallAPK()
                    time.sleep(2)
                    self.appOperation.installAPK(self.getApkName())
                    time.sleep(15)
                    doInThread(self.registerEvent.inputListener, self.d, 0, self.serNum)
                else:
                    self.appOperation.clearData()
                    time.sleep(3)
                self.startApp.startAPP(self.d, 15, first_dir + '/' + str(index) + '.mp4')
                time.sleep(15)
                MLog.info(u"等待清除缓存...")
                if self.machineName == "PACM00":
                    os.system('adb -s ' + self.serNum + ' shell service call statusbar 1')
                    self.d(text="停止录屏").click()
            time.sleep(10)
            if self.machineName == "PACM00":
                self.videoOperation.pullRecord("/sdcard/DCIM/Screenshots")
            else:
                self.videoOperation.pullRecord(first_dir)
            path = os.path.abspath('.')
            folder = path + '/' + first_dir
            MLog.debug(u"screen_record_main firstLaunch: folder = " + folder)
            os.chdir(folder)
            self.appOperation.killProcess()
            for index in range(int(self.getFirstStartTime())):
                self.videoOperation.videoToPhoto(str(first_dir + "_" + str(index)), str(index))
            os.chdir(path)

    # 首次启动,手动安装
    def firstLaunch2(self):
        if self.getFirstStartTime() > 0:
            if self.machineName == "PACM00":
                self.fileOperation.removeDirs("/sdcard/DCIM/Screenshots")
                MLog.info(u"删除 screenshot")
                path = os.path.dirname(__file__) + "\\"
                MLog.debug(u"screen_record_main firstLaunch: path = " + path)
                os.chdir(path)
                if os.path.exists("Screenshots"):
                    shutil.rmtree("Screenshots")

            first_dir = self.tempDir + "_first"
            self.fileOperation.mkdir(first_dir)

            for index in range(int(self.getFirstStartTime())):
                if self.machineName == "PACM00":
                    self.appOperation.uninstallAPK()
                    time.sleep(2)
                    self.appOperation.installAPK(self.getApkName())
                    time.sleep(15)
                    doInThread(self.registerEvent.inputListener, self.d, 0, self.serNum)
                else:
                    self.appOperation.clearData()
                    time.sleep(3)
                self.startApp.startAPP(self.d, 15, first_dir + '/' + str(index) + '.mp4')
                time.sleep(15)
                MLog.info(u"等待清除缓存...")
                if self.machineName == "PACM00":
                    os.system('adb -s ' + self.serNum + ' shell service call statusbar 1')
                    self.d(text="停止录屏").click()
            time.sleep(10)
            if self.machineName == "PACM00":
                self.videoOperation.pullRecord("/sdcard/DCIM/Screenshots")
            else:
                self.videoOperation.pullRecord(first_dir)
            path = os.path.abspath('.')
            folder = path + '/' + first_dir
            MLog.debug(u"screen_record_main firstLaunch: folder = " + folder)
            os.chdir(folder)
            self.appOperation.killProcess()
            for index in range(int(self.getFirstStartTime())):
                self.videoOperation.videoToPhoto(str(first_dir + "_" + str(index)), str(index))
            os.chdir(path)

    # 非首次启动
    def notFirstLaunch(self):
        if self.getNormalStartTime() > 0:
            if self.machineName == "PACM00":
                self.fileOperation.removeDirs("/sdcard/DCIM/Screenshots")
                MLog.info(u"删除 screenshot")
                path = os.path.dirname(__file__) + "\\"
                print path
                os.chdir(path)
                if os.path.exists("Screenshots"):
                    shutil.rmtree("Screenshots")

            notfirst_dir = self.tempDir + "_notfirst"
            self.fileOperation.mkdir(notfirst_dir)
            for index in range(int(self.getNormalStartTime())):

                self.appOperation.killProcess()
                self.startApp.startAPP(self.d, 15, notfirst_dir + '/' + str(index) + ".mp4")
                time.sleep(15)
                if self.machineName == "PACM00":
                    os.system('adb -s ' + self.serNum + ' shell service call statusbar 1')
                    self.d(text="停止录屏").click()
            time.sleep(10)
            if self.machineName == "PACM00":
                self.videoOperation.pullRecord("/sdcard/DCIM/Screenshots")
            else:
                self.videoOperation.pullRecord(notfirst_dir)
            path = os.path.abspath('.')
            folder = path + '/' + notfirst_dir
            MLog.debug(u"screen_record_main notFirstLaunch: path = " + path)
            os.chdir(folder)
            self.appOperation.killProcess()
            for index in range(int(self.getNormalStartTime())):
                self.videoOperation.videoToPhoto(str(notfirst_dir + "_" + str(index)), str(index))
            os.chdir(path)

    def start(self):
        os.system(
            'adb -s ' + self.serNum + ' shell monkey -p ' + self.getPackage() + ' -c android.intent.category.LAUNCHER 1 ')

    # 进入直播间
    def enterLiveRoom(self):
        # 启动APP
        self.startApp.startAPP(self.getPackage(), self.serNum)
        time.sleep(15)
        if self.getEnterLiveRoom() > 0:
            if self.machineName == "PACM00":
                self.fileOperation.removeDirs("/sdcard/DCIM/Screenshots")
                MLog.info(u"删除 screenshot")
                path = os.path.dirname(__file__) + "\\"
                MLog.debug(u"screen_record_main enterLiveRoom: path = " + path)
                os.chdir(path)
                if os.path.exists("Screenshots"):
                    shutil.rmtree("Screenshots")

            enter_dir = self.tempDir + "_enterliveroom"
            self.fileOperation.mkdir(enter_dir)
            for index in range(int(self.getEnterLiveRoom())):
                self.startApp.enter(self.d, 10, enter_dir + '/' + str(index) + ".mp4", self.serNum)
                time.sleep(5)
                if self.machineName == "PACM00":
                    os.system('adb -s ' + self.serNum + ' shell service call statusbar 1')
                    self.d(text="停止录屏").click()
            time.sleep(5)
            if self.machineName == "PACM00":
                self.videoOperation.pullRecord("/sdcard/DCIM/Screenshots")
            else:
                self.videoOperation.pullRecord(enter_dir)
            path = os.path.abspath('.')
            folder = path + '/' + enter_dir
            MLog.debug(u"screen_record_main enterLiveRoom: path2 = " + path)
            os.chdir(folder)
            self.appOperation.killProcess()
            for index in range(int(self.getEnterLiveRoom())):
                self.videoOperation.videoToPhoto(str(enter_dir + "_" + str(index)), str(index))
            os.chdir(path)
