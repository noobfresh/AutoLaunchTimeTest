# -*- coding: UTF-8 -*-

import sys
from uiautomator import Device
from register_event import *
from start_app import startAPP
from file_related import *
from app_stop_related import *
from video_related import *
from device_info import getDeviceInfo

# 解决即使把adb加入到了path，python也调不到的问题（为了使用UIAutomator引入的）
os.environ.__delitem__('ANDROID_HOME')
os.environ.__setitem__('ANDROID_HOME', 'C:/Android/')
os.environ.update()

conf = Config("default.ini")

# 常量初始化
save_dir = '/sdcard/screenrecord/'

# 这个要换成设备名称
# temp_dir = ''
# 手机名称
deviceList = []
serial = []


def getDevice():
    global deviceList
    global serial
    conf = Config("default.ini")
    event = conf.getconf("serial").serial_number
    serial = event.split(',')
    print serial
    for index in range(len(serial)):
        deviceList.append(Device(serial[index]))


# 首次启动
def firstLaunch(d, firstLaunchTimes, apkName, temp_dir, sernum, machineName):
    if firstLaunchTimes > 0:
        if machineName == "PACM00":
            removeDirs("/sdcard/DCIM/Screenshots", sernum)
            print u"删除 screenshot==="
            path = os.path.abspath('.')
            print path
            os.chdir(path)
            if os.path.exists("Screenshots"):
                shutil.rmtree("Screenshots")
        uninstallAPK(sernum)
        # firstTimes = firstLaunchTimes * 20
        first_dir = temp_dir + "_first"
        mkdir(first_dir, sernum)
        if machineName != "PACM00":
            installAPK(apkName, sernum)
            time.sleep(15)  # 后续改成轮询是否有安装包的包名，有再录屏
        # screenRecord(firstTimes, first_dir + '/' + 'first.mp4')
        # startTime = time.time()
        for index in range(firstLaunchTimes):
            if machineName == "PACM00":
                uninstallAPK(sernum)
                time.sleep(2)
                installAPK(apkName, sernum)
                time.sleep(15)
                doInThread(inputListener, d, 0, sernum)
            else:
                clearData(sernum)
                time.sleep(3)
            startAPP(d, 15, first_dir + '/' + str(index) + '.mp4', sernum, machineName)
            time.sleep(15)
            if machineName == "PACM00":
                os.system('adb -s ' + sernum + ' shell service call statusbar 1')
                d(text="停止录屏").click()
        # endTime = time.time()
        # if firstTimes > int(endTime - startTime):
        #     print u'尚未录制结束'
        #     time.sleep(firstTimes - int(endTime - startTime) + 1)
        time.sleep(10)
        if machineName == "PACM00":
            pullRecord("/sdcard/DCIM/Screenshots", sernum, machineName)
        else:
            pullRecord(first_dir, sernum, machineName)
        path = os.path.abspath('.')
        folder = path + '/' + first_dir
        print "====" + folder
        os.chdir(folder)
        killProcess(sernum)
        for index in range(firstLaunchTimes):
            videoToPhoto(str(first_dir + "_" + str(index)), str(index), machineName)
        os.chdir(path)


# 非首次启动
def notFirstLaunch(d, notFirstLaunchTimes, temp_dir, sernum, machineName):
    if notFirstLaunchTimes > 0:
        if machineName == "PACM00":
            removeDirs("/sdcard/DCIM/Screenshots", sernum)
            print u"删除 screenshot==="
            path = os.path.abspath('.')
            print path
            os.chdir(path)
            if os.path.exists("Screenshots"):
                shutil.rmtree("Screenshots")

        notfirst_dir = temp_dir + "_notfirst"
        mkdir(notfirst_dir, sernum)
        # notfirstTimes = notFirstLaunchTimes * 15
        # screenRecord(notfirstTimes, notfirst_dir + '/' + 'notfirst.mp4')
        # startTime = time.time()
        for index in range(notFirstLaunchTimes):
            """
            grantPermission()
            time.sleep(2)
            """

            killProcess(sernum)
            startAPP(d, 15, notfirst_dir + '/' + str(index) + ".mp4", sernum, machineName)
            time.sleep(15)
            if machineName == "PACM00":
                os.system('adb -s ' + sernum + ' shell service call statusbar 1')
                d(text="停止录屏").click()
        # endTime = time.time()
        # if firstTimes > int(endTime - startTime):
        #     print u'尚未录制结束'
        #     time.sleep(firstTimes - int(endTime - startTime) + 1)
        time.sleep(10)
        if machineName == "PACM00":
            pullRecord("/sdcard/DCIM/Screenshots", sernum, machineName)
        else:
            pullRecord(notfirst_dir, sernum, machineName)
        path = os.path.abspath('.')
        folder = path + '/' + notfirst_dir
        print "====" + folder
        os.chdir(folder)
        killProcess(sernum)
        for index in range(notFirstLaunchTimes):
            videoToPhoto(str(notfirst_dir + "_" + str(index)), str(index), machineName)
        os.chdir(path)


# main函数，线程sleep时间有待商榷
def main(d, firstLaunchTimes, notFirstLaunchTimes, apkName, temp_dir, sernum):
    machineName = getDeviceInfo(sernum)
    firstLaunchTimes = int(firstLaunchTimes)
    notFirstLaunchTimes = int(notFirstLaunchTimes)
    print "times1 = {}, times2 = {}, apkName = {}".format(str(firstLaunchTimes), str(notFirstLaunchTimes), apkName)
    firstLaunch(d, firstLaunchTimes, apkName, temp_dir, sernum, machineName)
    notFirstLaunch(d, notFirstLaunchTimes, temp_dir, sernum, machineName)


def start_python(firstLaunchTimes, notFirstLaunchTimes, apkName):
    # for index in range(len(deviceList)):
    getDevice()
    for index in range(len(deviceList)):
        d = deviceList[index]
        serNum = serial[index]
        print serNum + "444444444444"
        temp_dir = getDeviceInfo(serNum)
        d.wakeup()
        thread1 = doInThread(runwatch, d, 0)
        time.sleep(30)
        thread2 = doInThread(inputListener, d, 0, serNum)
        # thread3 = doInThread(main, d, sys.argv[1], sys.argv[2], sys.argv[3], temp_dir, serNum)
        main(d, firstLaunchTimes, notFirstLaunchTimes, apkName, temp_dir, serNum)


if __name__ == "__main__":
    getDevice()
    for index in range(len(deviceList)):
        d = deviceList[index]
        serNum = serial[index]
        print serNum + "444444444444"
        temp_dir = getDeviceInfo(serNum)
        d.wakeup()
        thread1 = doInThread(runwatch, d, 0)
        time.sleep(30)
        thread2 = doInThread(inputListener, d, 0, serNum)
        # 加上下面两行
        settings._init()
        settings.set_value("ffmpeg", 30)
        # thread3 = doInThread(main, d, sys.argv[1], sys.argv[2], sys.argv[3], temp_dir, serNum)
        main(d, sys.argv[1], sys.argv[2], sys.argv[3], temp_dir, serNum)

    # os.system("adb shell input swipe 633 1448 634 1448 10")

# 问题：多设备连接
