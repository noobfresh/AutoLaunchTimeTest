# -*- coding: UTF-8 -*-

import sys
# from uiautomator import Device
import uiautomator2 as u2

import settings
from register_event import *
from start_app import startAPP
from file_operation import *
from app_operation import *
from video_operation import *
from device_info import getDeviceInfo
from multiprocessing import Pool
from start_app import enter

# 解决即使把adb加入到了path，python也调不到的问题（为了使用UIAutomator引入的）
os.environ.__delitem__('ANDROID_HOME')
os.environ.__setitem__('ANDROID_HOME', 'C:/Android/')
os.environ.update()

conf = Config("default.ini")

# 序列号
serial = []


def getDevices():
    devices = subprocess.Popen('adb devices'.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    for item in devices.split():
        filters = ['list', 'of', 'device', 'devices', 'attached']
        if item.lower() not in filters:
            serial.append(item)
    return serial


# 首次启动
def firstLaunch(d, firstLaunchTimes, apkName, temp_dir, sernum, machineName):
    if firstLaunchTimes > 0:
        if machineName == "PACM00":
            removeDirs("/sdcard/DCIM/Screenshots", sernum)
            print u"删除 screenshot==="
            path = os.path.dirname(__file__) + "\\"
            print path
            os.chdir(path)
            if os.path.exists("Screenshots"):
                shutil.rmtree("Screenshots")
        uninstallAPK(sernum)
        print 'executing uninstall' + sernum
        # firstTimes = firstLaunchTimes * 20
        first_dir = temp_dir + "_first"
        mkdir(first_dir, sernum)
        if machineName != "PACM00":
            installAPK(apkName, sernum)
            time.sleep(20)  # 后续改成轮询是否有安装包的包名，有再录屏
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
            path = os.path.dirname(__file__) + "\\"
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


def start(packageName, serNum):
    os.system('adb -s ' + serNum + ' shell monkey -p ' + packageName + ' -c android.intent.category.LAUNCHER 1 ')


# 进入直播间
def enterLiveRoom(d, enterLiveRoomTimes, temp_dir, sernum, machineName):
    print '===enterLiveRoom==='
    packageName = conf.getconf("default").package
    # 启动APP
    start(packageName, sernum)
    time.sleep(15)
    if enterLiveRoomTimes > 0:
        if machineName == "PACM00":
            removeDirs("/sdcard/DCIM/Screenshots", sernum)
            print u"删除 screenshot==="
            path = os.path.dirname(__file__) + "\\"
            print path
            os.chdir(path)
            if os.path.exists("Screenshots"):
                shutil.rmtree("Screenshots")

        enter_dir = temp_dir + "_enterliveroom"
        mkdir(enter_dir, sernum)
        for index in range(enterLiveRoomTimes):
            enter(d, 10, enter_dir + '/' + str(index) + ".mp4", sernum, machineName, packageName)
            time.sleep(5)
            if machineName == "PACM00":
                os.system('adb -s ' + sernum + ' shell service call statusbar 1')
                d(text="停止录屏").click()
        time.sleep(5)
        if machineName == "PACM00":
            pullRecord("/sdcard/DCIM/Screenshots", sernum, machineName)
        else:
            pullRecord(enter_dir, sernum, machineName)
        path = os.path.abspath('.')
        folder = path + '/' + enter_dir
        print "====" + folder
        os.chdir(folder)
        killProcess(sernum)
        for index in range(enterLiveRoomTimes):
            videoToPhoto(str(enter_dir + "_" + str(index)), str(index), machineName)
        os.chdir(path)


# main函数，线程sleep时间有待商榷
def screenmain(firstLaunchTimes, notFirstLaunchTimes, enterLiveTimes, apkName, temp_dir, sernum):
    print 'start main---' + sernum
    settings._init()
    try:
        d = u2.connect(sernum)
        # d = Device(sernum)
        print d.device_info
        print 'test....'
        doInThread(runwatch, d, 0)
        time.sleep(10)
        print 'test....1'
        doInThread(inputListener, d, 0, sernum)
        print 'test....2'
        time.sleep(20)
        machineName = getDeviceInfo(sernum)
        firstLaunchTimes = int(firstLaunchTimes)
        notFirstLaunchTimes = int(notFirstLaunchTimes)
        enterLiveTimes = int(enterLiveTimes)
        print "===screen record main ====times1 = {}, times2 = {}, apkName = {}".format(str(firstLaunchTimes),
                                                                                        str(notFirstLaunchTimes),
                                                                                        apkName)
        firstLaunch(d, firstLaunchTimes, apkName, temp_dir, sernum, machineName)
        notFirstLaunch(d, notFirstLaunchTimes, temp_dir, sernum, machineName)
        enterLiveRoom(d, enterLiveTimes, temp_dir, sernum, machineName)
    except BaseException, e:
        print repr(e)

    print 'end main'


# 改成单个
def start_python(firstLaunchTimes, notFirstLaunchTimes, enterLiveTimes, apkName, serial_num):
    print serial_num + "   444444444444"
    temp_dir = getDeviceInfo(serial_num)
    screenmain(firstLaunchTimes, notFirstLaunchTimes, enterLiveTimes, apkName, temp_dir, serial_num)


if __name__ == "__main__":
    getDevices()
    p = Pool(5)
    for index in range(len(serial)):
        serNum = serial[index]
        print serNum + "444444444444" + sys.argv[1] + " " + sys.argv[2]
        temp_dir = getDeviceInfo(serNum)
        # 加上下面两行
        settings._init()
        settings.set_value("ffmpeg", 30)
        p.apply_async(screenmain, args=(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], temp_dir, serNum,))
    p.close()
    p.join()
