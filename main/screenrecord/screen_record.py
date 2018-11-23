# -*- coding: UTF-8 -*-

import os
import subprocess
import time
import shutil
import threading
import re
from uiautomator import Device
from uiautomator import device as d
import sys
import settings
from config.configs import Config

# 解决即使把adb加入到了path，python也调不到的问题（为了使用UIAutomator引入的）
from log.log import MLog

os.environ.__delitem__('ANDROID_HOME')
os.environ.__setitem__('ANDROID_HOME', 'C:/Android')
os.environ.update()

# 常量初始化
apkName = 'yy.apk'
packageName = 'com.duowan.mobile'
save_dir = '/sdcard/screenrecord/'
# 这个要换成设备名称
temp_dir = 'yy'
# 手机名称
machineName = ''
deviceList = []
startTime = time.time()
endTime = time.time()


def getDevice(series):
    global deviceList
    for index in range(len(series)):
        deviceList[index] = Device(series[index])


# 拿设备信息防止文件夹重名
def getDeviceInfo():
    global machineName
    deviceName = os.popen('adb shell getprop ro.product.model').read()
    deviceName = re.sub('\s', '', deviceName)
    global temp_dir
    temp_dir = checkNameValid(deviceName.strip('\n'))
    machineName = deviceName
    print "machine name = {}".format(deviceName)
    return deviceName


# 安装应用
def installAPK(name):
    path = os.path.dirname(__file__) + "\\"
    os.chdir(path)
    print path
    os.system("adb install " + name)
    print u'安装成功'


# 授权,不生效,弃用
def grantPermission():
    os.system('adb shell pm grant ' + packageName + ' android.permission.READ_CONTACTS')
    os.system('adb shell pm grant ' + packageName + ' android.permission.INTERNET')
    os.system('adb shell pm grant ' + packageName + ' android.permission.RECEIVE_SMS')
    os.system('adb shell pm grant ' + packageName + ' android.permission.ACCESS_MOCK_LOCATION')
    os.system('adb shell pm grant ' + packageName + ' android.permission.ACCESS_NETWORK_STATE')
    os.system('adb shell pm grant ' + packageName + ' android.permission.ACCESS_FINE_LOCATION')
    os.system('adb shell pm grant ' + packageName + ' android.permission.ACCESS_COARSE_LOCATION')
    os.system('adb shell pm grant ' + packageName + ' android.permission.READ_PHONE_STATE')
    os.system('adb shell pm grant ' + packageName + ' android.permission.SEND_SMS')
    os.system('adb shell pm grant ' + packageName + ' android.permission.WRITE_EXTERNAL_STORAGE')
    os.system('adb shell pm grant ' + packageName + ' android.permission.READ_EXTERNAL_STORAGE')
    print u'授权成功'


# 录屏
def screenRecord(times, name):
    subprocess.Popen("adb shell screenrecord --time-limit " + str(times) + " " + save_dir + name)
    print u'录屏开始'


# 数据上传
def pullRecord(name):
    print save_dir + name
    os.system('adb pull ' + save_dir + name)
    print u'数据上传成功'


# 创建文件夹
def mkdir(name):
    os.system('adb shell rm -rf ' + save_dir + name)
    os.system('adb shell mkdir -p ' + save_dir + name)
    print u'SD卡文件夹创建成功'
    path = os.path.abspath('.')
    os.chdir(path)
    if os.path.exists(name):
        shutil.rmtree(name)
    print name
    os.makedirs(name)
    print u'PC文件夹创建成功'


# Windows文件名检查
def checkNameValid(name=None):
    if name is None:
        print("name is None!")
        return
    reg = re.compile(r'[\\/:*?"<>|\s\r\n]+')
    valid_name = reg.findall(name)
    if valid_name:
        for nv in valid_name:
            name = name.replace(nv, "")
    return name


# 启动应用
def startAPP(times, video):
    # os.system('adb shell monkey -p '+packageName+' -c android.intent.category.LAUNCHER 1')
    try:
        print u"尝试启动app"
        startAppBySwipe(times, video)
    except:
        print u"启动app失败！"

    # os.system('adb shell monkey -p '+packageName+' -c android.intent.category.LAUNCHER 1')
    # try:
    #     print "--------start app1"
    #     d(text='YY').click()
    # except:
    #     try:
    #         print "--------start app2"
    #         d(text='@YY').click()
    #     except:
    #         print u"启动失败"


def startAppBySwipe(times, video):
    global startTime
    try:
        pos = d(text="YY").bounds
        print u"start YY"
    except:
        pos = d(text="@YY").bounds
        print u"start @YY"

    print "----------->"
    print pos
    # offset代表偏移量，方便点中logo中间部分
    startTime = time.time()
    screenRecord(times, video)
    time.sleep(2)
    offset = 0
    x = pos['left'] + offset
    y = pos['top'] + offset
    start_shell = "adb shell input swipe " + str(x) + " " + str(y) + " " + str(int(x) + 10) + " " + str(y) + " 10"
    print start_shell
    os.system(start_shell)


# 杀进程
def killProcess():
    os.system('adb shell am force-stop ' + packageName)
    print '---kill process ---'


# 清除数据
def clearData():
    os.system('adb shell pm clear ' + packageName)
    print u'清除数据'


# 卸载应用
def uninstallAPK():
    os.system('adb uninstall ' + packageName)


def utf8(file_name):
    return file_name.decode('utf-8')


# 注册一些点击事件
def registerEvent(d):
    print u"registerEvent"
    conf = Config("default.ini")
    event = conf.getconf("common").click_event
    # print event
    MLog.debug("event = " + event)
    num = event.split(',')
    for index in range(0, num.__len__()):
        key = 'event' + str(index)
        item = utf8(num[index])
        MLog.debug("key = " + key + " and " + "item = " + item)
        d.watcher(key).when(text=item).click(text=item)

    MLog.debug(u"列出所有watchers")
    print d.watchers


# 视频转换成帧
# ffmpeg没有视频切成帧输出到指定目录的命令，只能反复调工作目录
def videoToPhoto(dirname, index):
    curPath = os.getcwd()
    print '+++++++++++++' + curPath
    if os.path.isdir(dirname):
        os.removedirs(dirname)
    os.makedirs(dirname)
    chagePath = curPath + '/' + dirname
    print '+++++++++++++' + chagePath
    os.chdir(chagePath)
    print "帧数 = " + str(settings.get_value("ffmpeg"))
    strcmd = 'ffmpeg -i ' + curPath + '/' + index + '.mp4' + ' -r ' + str(
        settings.get_value("ffmpeg")) + ' -f ' + 'image2 %05d.jpg'
    subprocess.call(strcmd, shell=True)
    os.chdir(curPath)


# 线程函数,用来运行一些watcher，事件监听
class FuncThread(threading.Thread):
    def __init__(self, func, *params, **paramMap):
        threading.Thread.__init__(self)
        self.func = func
        self.params = params
        self.paramMap = paramMap
        self.rst = None
        self.finished = False

    def run(self):
        self.rst = self.func(*self.params, **self.paramMap)
        self.finished = True

    def getResult(self):
        return self.rst

    def isFinished(self):
        return self.finished

    def isStopped(self):
        return self.stopped


# 启动子线程运行一些func
def doInThread(func, *params, **paramMap):
    t_setDaemon = None
    if 't_setDaemon' in paramMap:
        t_setDaemon = paramMap['t_setDaemon']
        del paramMap['t_setDaemon']
    ft = FuncThread(func, *params, **paramMap)
    if t_setDaemon != None:
        ft.setDaemon(t_setDaemon)
    ft.start()
    return ft


# 运行点击事件
def runwatch(d, data):
    registerEvent(d)
    while True:
        if data == 1:
            return True
        # d.watchers.reset()
        d.watchers.run()


# 通过配置文件获取密码
def getPwdByConfig(device_name):
    conf = Config("device.ini")
    pwd = conf.getconf(device_name).password
    print "device_name = " + str(device_name) + " and " + "pwd = " + str(pwd)
    return pwd


# 监听输入密码
def inputListener(d, data):
    machineName = getDeviceInfo()
    if machineName == "OPPOR11Plusk":
        if d(className="android.widget.EditText",
             resourceId="com.coloros.safecenter:id/et_login_passwd_edit").wait.exists(timeout=50000):
            d(className="android.widget.EditText",
              resourceId="com.coloros.safecenter:id/et_login_passwd_edit").set_text(
                getPwdByConfig(machineName))
        if d(className="android.widget.LinearLayout",
             resourceId="com.android.packageinstaller:id/bottom_button_layout").wait.exists(timeout=50000):
            d.click(458, 1602)
    print 1

    if machineName == "OPPOR9s":
        if d(className="android.widget.EditText",
             resourceId="com.coloros.safecenter:id/et_login_passwd_edit").wait.exists(timeout=50000):
            d(className="android.widget.EditText",
              resourceId="com.coloros.safecenter:id/et_login_passwd_edit").set_text(
                getPwdByConfig(machineName))
        if d(className="android.widget.LinearLayout",
             resourceId="com.android.packageinstaller:id/bottom_button_layout").wait.exists(timeout=50000):
            d.click(696, 1793)
    print 2

    if machineName == "PACM00":
        if d(className="android.widget.LinearLayout",
             resourceId="com.android.packageinstaller:id/bottom_button_layout").wait.exists(timeout=50000):
            d.click(458, 1900)
    print 3

    if machineName == "OPPOA59a":
        if d(className="android.widget.EditText", resourceId="com.coloros.safecenter:id/verify_input").wait.exists(
                timeout=50000):
            d(className="android.widget.EditText", resourceId="com.coloros.safecenter:id/verify_input").set_text(
                getPwdByConfig(machineName))

    print 4

    if machineName == "OPPOA83":
        MLog.debug(getPwdByConfig(machineName))
        if d(className="android.widget.EditText",
             resourceId="com.coloros.safecenter:id/et_login_passwd_edit").wait.exists(
            timeout=50000):
            d(className="android.widget.EditText",
              resourceId="com.coloros.safecenter:id/et_login_passwd_edit").set_text(
                getPwdByConfig(machineName))
            MLog.debug("===input password ====")

    print 5

    if machineName == "MI8":
        MLog.debug("MI8")
        MLog.debug(getPwdByConfig(machineName))
        if d(className="android.widget.Button",
             resourceId="android:id/button2").wait.exists(
            timeout=50000):
            MLog.debug("安装界面")
            d.click(50, 2800)

    print 6


# main函数，线程sleep时间有待商榷
def main(firstLaunchTimes, notFirstLaunchTimes, apkName):
    getDeviceInfo()
    global endTime
    global startTime
    global temp_dir
    firstLaunchTimes = int(firstLaunchTimes)
    notFirstLaunchTimes = int(notFirstLaunchTimes)
    print "times1 = {}, times2 = {}, apkName = {}".format(str(firstLaunchTimes), str(notFirstLaunchTimes), apkName)
    if firstLaunchTimes > 0:
        uninstallAPK()
        firstTimes = firstLaunchTimes * 20
        first_dir = temp_dir + "_first"
        mkdir(first_dir)
        installAPK(apkName)
        time.sleep(30)  # 后续改成轮询是否有安装包的包名，有再录屏
        # screenRecord(firstTimes, first_dir + '/' + 'first.mp4')
        #startTime = time.time()
        for index in range(firstLaunchTimes):
            clearData()
            time.sleep(3)
            startAPP(firstTimes, first_dir + '/' + 'first.mp4')
            time.sleep(20)
        endTime = time.time()
        if firstTimes > int(endTime - startTime):
            print u'尚未录制结束'
            time.sleep(firstTimes - int(endTime - startTime) + 1)
        pullRecord(first_dir)
        path = os.path.abspath('.')
        folder = path + '/' + first_dir
        print "====" + folder
        os.chdir(folder)
        killProcess()

        videoToPhoto(str(first_dir + "_" + "first"), "first")
        os.chdir(path)

    if notFirstLaunchTimes > 0:
        notfirst_dir = temp_dir + "_notfirst"
        mkdir(notfirst_dir)
        notfirstTimes = notFirstLaunchTimes * 15
        # screenRecord(notfirstTimes, notfirst_dir + '/' + 'notfirst.mp4')
        #startTime = time.time()
        for index in range(notFirstLaunchTimes):
            """
            grantPermission()
            time.sleep(2)
            """

            killProcess()
            startAPP(notfirstTimes, notfirst_dir + '/' + 'notfirst.mp4')
            time.sleep(20)
        endTime = time.time()
        if firstTimes > int(endTime - startTime):
            print u'尚未录制结束'
            time.sleep(firstTimes - int(endTime - startTime) + 1)
        pullRecord(notfirst_dir)
        path = os.path.abspath('.')
        folder = path + '/' + notfirst_dir
        print "====" + folder
        os.chdir(folder)
        killProcess()
        videoToPhoto(str(notfirst_dir + "_" + "notfirst"), "notfirst")
        os.chdir(path)


def start_python(firstLaunchTimes, notFirstLaunchTimes, apkName):
    thread1 = doInThread(runwatch, d, 0)
    thread2 = doInThread(inputListener, d, 0)
    main(firstLaunchTimes, notFirstLaunchTimes, apkName)


if __name__ == "__main__":
    thread1 = doInThread(runwatch, d, 0)
    thread2 = doInThread(inputListener, d, 0)
    time.sleep(30)
    # 加上下面两行
    settings._init()
    settings.set_value("ffmpeg", 30)
    main(sys.argv[1], sys.argv[2], sys.argv[3])

    # os.system("adb shell input swipe 633 1448 634 1448 10")

# 问题：多设备连接
