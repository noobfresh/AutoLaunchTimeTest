# -*- coding: UTF-8 -*-

import os
import re
import shutil
import subprocess
import sys
import threading
import time

from uiautomator import Device
from uiautomator import device as d

import settings
from calculate.template_match import findLaunchLogo
from config.configs import Config
# 解决即使把adb加入到了path，python也调不到的问题（为了使用UIAutomator引入的）
from log.log import MLog
from screenrecord.screencap import cap

os.environ.__delitem__('ANDROID_HOME')
os.environ.__setitem__('ANDROID_HOME', 'C:/Users/Administrator/AppData/Local/Android/Sdk/')
os.environ.update()

conf = Config("default.ini")
package = conf.getconf("default").package

# 常量初始化
packageName = package
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
    if machineName == "PACM00":
        os.system('adb shell service call statusbar 1')
        d(text="开始录屏").click()
        print "start"
        time.sleep(5)
    else:
        print(name + "         ----------------------------------                ---------------------------")
        subprocess.Popen("adb shell screenrecord --time-limit " + str(times) + " " + save_dir + name)
    print u'录屏开始'


# 数据上传
def pullRecord(name):
    if machineName == "PACM00":
        os.system("adb pull " + name)
    else:
        print save_dir + name
        os.system('adb pull ' + save_dir + name)
        print u'数据上传成功'


# 创建文件夹
def mkdir(name):
    os.system('adb shell rm -rf ' + save_dir + name)
    os.system('adb shell mkdir -p ' + save_dir + name)
    print u'SD卡文件夹创建成功'
    path = os.path.dirname(__file__) + "\\"
    os.chdir(path)
    print u'创建文件夹' + path
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
        MLog.debug(u"尝试启动app")
        startAppBySwipe(times, video)
    except Exception, e:
        print repr(e)
        MLog.debug(u"startAPP:" + u"启动app失败！")
        sys.exit(-1)

def getPos(app_name):
    machineName = getDeviceInfo()
    conf = Config("apk.ini")
    conf_default = Config("default.ini")
    app_key = conf_default.getconf("default").app
    feature_dir = conf.getconf(str(app_key)).feature
    if machineName == "vivoX9":
        MLog.info("get pos by cap findLaunchLogo")
        pos = findLaunchLogo(cap(), "../picrepos/feature/" + feature_dir + "/vivoX9_launch_feature.jpg")
    elif machineName == "vivoX7":
        MLog.info("get pos by cap findLaunchLogo")
        pos = findLaunchLogo(cap(), "../picrepos/feature/" + feature_dir + "/vivoX7_launch_feature.jpg")
    else:
        MLog.debug("get pos by uiautomator")
        pos = d(text=app_name).bounds
    settings.set_value("pos", pos)
    return pos


def startAppBySwipe(times, video):
    global startTime
    conf = Config("default.ini")
    app_name = conf.getconf("default").app_name

    try:
        MLog.info("startAppBySwipe:" + u"try start app ,name = " + app_name)
        pos = settings.get_value("pos", None)
        if pos is None:
            pos = getPos(app_name)
    except Exception, e:
        MLog.info(repr(e))
        app_name = "@" + app_name
        pos = getPos(app_name)

    MLog.debug("startAppBySwipe:" + str(pos))
    # offset代表偏移量，方便点中logo中间部分
    startTime = time.time()
    screenRecord(times, video)
    time.sleep(2)
    offset = 0
    left = pos['left'] + offset
    top = pos['top'] + offset
    right = pos['right']
    bottom = pos['bottom']

    x = (left + right) >> 1
    y = (top + bottom) >> 1
    duration = 10
    start_shell = "adb shell input swipe " + str(x) + " " + str(y) + " " + str(x + 1) + " " + str(y) + " " + str(
        duration)
    MLog.info(start_shell)
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
    d.watchers.remove()
    print u"registerEvent" + str(d.watchers)
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
    if machineName == "PACM00":
        print str(curPath) + "-------------"

        srcPath = os.path.join(os.path.dirname(curPath), "Screenshots")
        print srcPath + "1111111111"
        count = 0
        # for filename in os.listdir(srcPath):
        os.chdir(srcPath)

        for root, dirs, files in os.walk(srcPath):  # 遍历统计
            for file in files:
                print os.path.abspath(file)
                shutil.copyfile(file, curPath + "/" + str(count) + ".mp4")
                count += 1
        # shutil.copytree(os.path.join(os.path.dirname(curPath), "Screenshots"), curPath)
        # rename_mp4_files(curPath)
        os.chdir(curPath)

    print '+++++++++++++' + curPath
    if os.path.isdir(dirname):
        # os.removedirs(dirname)
        shutil.rmtree(dirname)
    os.makedirs(dirname)
    chagePath = curPath + '/' + dirname
    print '+++++++++++++' + chagePath
    os.chdir(chagePath)
    print u"帧数 = " + str(settings.get_value("ffmpeg"))
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


def getWatchNum():
    conf = Config("default.ini")
    event = conf.getconf("common").click_event
    # print event
    MLog.debug("event = " + event)
    num = event.split(',')
    return len(num)


# 运行点击事件
def runwatch(d, data):
    registerEvent(d)
    num = getWatchNum()
    while True:
        if len(d.watchers) != num:
            registerEvent(d)
        d.watchers.run()


# 通过配置文件获取密码
def getPwdByConfig(device_name):
    conf = Config("device.ini")
    pwd = conf.getconf(device_name).password
    print "device_name = " + str(device_name) + " and " + "pwd = " + str(pwd)
    return pwd


def click_with_pos(class_name, res_id, pos_x, pos_y):
    if d(className=class_name,
         resourceId=res_id).wait.exists(timeout=50000):
        MLog.debug("click_with_pos:" + "x = " + str(pos_x) + "  y =" + str(pos_y))
        d.click(pos_x, pos_y)


def click_with_id(class_name, res_id):
    if d(className=class_name,
         resourceId=res_id).wait.exists(timeout=50000):
        d(className=class_name,
          resourceId=res_id).click()


def set_text_with_id(class_name, res_id, text_content):
    if d(className=class_name,
         resourceId=res_id).wait.exists(timeout=50000):
        d(className=class_name,
          resourceId=res_id).set_text(text_content)


# 监听输入密码
def inputListener(d, data):
    machineName = getDeviceInfo()
    if machineName == "OPPOR11Plusk":
        # if d(className="android.widget.EditText",
        #      resourceId="com.coloros.safecenter:id/et_login_passwd_edit").wait.exists(timeout=50000):
        #     d(className="android.widget.EditText",
        #       resourceId="com.coloros.safecenter:id/et_login_passwd_edit").set_text(
        #         getPwdByConfig(machineName))
        set_text_with_id("android.widget.EditText", "com.coloros.safecenter:id/et_login_passwd_edit",
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
        if d(className="android.widget.EditText",
             resourceId="com.coloros.safecenter:id/et_login_passwd_edit").wait.exists(timeout=50000):
            d(className="android.widget.EditText",
              resourceId="com.coloros.safecenter:id/et_login_passwd_edit").set_text(
                getPwdByConfig(machineName))
        if d(className="android.widget.LinearLayout",
             resourceId="com.android.packageinstaller:id/bottom_button_layout").wait.exists(timeout=50000):
            d.click(458, 1900)
    print 3

    if machineName == "OPPOA59a":
        if d(className="android.widget.EditText", resourceId="com.coloros.safecenter:id/verify_input").wait.exists(
                timeout=50000):
            d(className="android.widget.EditText", resourceId="com.coloros.safecenter:id/verify_input").set_text(
                getPwdByConfig(machineName))
        if d(className="android.widget.LinearLayout",
             resourceId="com.android.packageinstaller:id/bottom_button_layout").wait.exists(timeout=50000):
            d.click(458, 1900)
    print 4

    if machineName == "OPPOA83":
        MLog.debug(getPwdByConfig(machineName))

        MLog.debug(u"输入密码界面")
        set_text_with_id("android.widget.EditText", "com.coloros.safecenter:id/et_login_passwd_edit",
                         getPwdByConfig(machineName))

        MLog.debug(u"来至电脑端未知来源，只能自己配[222, 1160]")
        click_with_pos("android.widget.LinearLayout", "com.android.packageinstaller:id/bottom_button_layout", 222, 1160)

        MLog.debug(u"完成")
        click_with_id("android.widget.TextView", "com.android.packageinstaller:id/done_button")

    print 5

    if machineName == "OPPOA57":
        set_text_with_id("android.widget.EditText", "com.coloros.safecenter:id/et_login_passwd_edit",
                         getPwdByConfig(machineName))
        if d(className="android.widget.LinearLayout",
             resourceId="com.android.packageinstaller:id/bottom_button_layout").wait.exists(timeout=50000):
            d.click(528, 1218)

    if machineName == "vivoX9":
        MLog.debug("vivoX9")
        click_with_pos("android.widget.Button", "vivo:id/vivo_adb_install_ok_button", 298, 1845)
    print 6


def removeDirs(dir):
    os.system('adb shell rm -rf ' + dir)


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
        if machineName == "PACM00":
            removeDirs("/sdcard/DCIM/Screenshots")
            print u"删除 screenshot==="
            path = os.path.abspath('.')
            print path
            os.chdir(path + "/screenrecord")
            if os.path.exists("Screenshots"):
                shutil.rmtree("Screenshots")
        uninstallAPK()
        # firstTimes = firstLaunchTimes * 20
        first_dir = temp_dir + "_first"
        mkdir(first_dir)
        if machineName != "PACM00":
            installAPK(apkName)
            time.sleep(15)  # 后续改成轮询是否有安装包的包名，有再录屏
        # screenRecord(firstTimes, first_dir + '/' + 'first.mp4')
        # startTime = time.time()
        for index in range(firstLaunchTimes):
            if machineName == "PACM00":
                uninstallAPK()
                time.sleep(2)
                installAPK(apkName)
                time.sleep(15)
                doInThread(inputListener, d, 0)
            else:
                clearData()
                time.sleep(3)
            startAPP(20, first_dir + '/' + str(index) + '.mp4')
            time.sleep(20)
            if machineName == "PACM00":
                os.system('adb shell service call statusbar 1')
                d(text="停止录屏").click()
        # endTime = time.time()
        # if firstTimes > int(endTime - startTime):
        #     print u'尚未录制结束'
        #     time.sleep(firstTimes - int(endTime - startTime) + 1)
        time.sleep(10)
        if machineName == "PACM00":
            pullRecord("/sdcard/DCIM/Screenshots")
        else:
            pullRecord(first_dir)
        path = os.path.abspath('.')
        folder = path + '/' + first_dir
        print "====" + folder
        os.chdir(folder)
        killProcess()
        for index in range(firstLaunchTimes):
            videoToPhoto(str(first_dir + "_" + str(index)), str(index))
        os.chdir(path)

    if notFirstLaunchTimes > 0:
        if machineName == "PACM00":
            removeDirs("/sdcard/DCIM/Screenshots")
            print u"删除 screenshot==="
            path = os.path.abspath('.')
            print path
            os.chdir(path)
            if os.path.exists("Screenshots"):
                shutil.rmtree("Screenshots")

        notfirst_dir = temp_dir + "_notfirst"
        mkdir(notfirst_dir)
        # notfirstTimes = notFirstLaunchTimes * 15
        # screenRecord(notfirstTimes, notfirst_dir + '/' + 'notfirst.mp4')
        # startTime = time.time()
        for index in range(notFirstLaunchTimes):
            """
            grantPermission()
            time.sleep(2)
            """

            killProcess()
            startAPP(20, notfirst_dir + '/' + str(index) + ".mp4")
            time.sleep(20)
            if machineName == "PACM00":
                os.system('adb shell service call statusbar 1')
                d(text="停止录屏").click()
        # endTime = time.time()
        # if firstTimes > int(endTime - startTime):
        #     print u'尚未录制结束'
        #     time.sleep(firstTimes - int(endTime - startTime) + 1)
        time.sleep(10)
        if machineName == "PACM00":
            pullRecord("/sdcard/DCIM/Screenshots")
        else:
            pullRecord(notfirst_dir)
        path = os.path.abspath('.')
        folder = path + '/' + notfirst_dir
        print "====" + folder
        os.chdir(folder)
        killProcess()
        for index in range(notFirstLaunchTimes):
            videoToPhoto(str(notfirst_dir + "_" + str(index)), str(index))
        os.chdir(path)


def start_python(firstLaunchTimes, notFirstLaunchTimes, apkName):
    thread1 = doInThread(runwatch, d, 0)
    thread2 = doInThread(inputListener, d, 0)
    time.sleep(30)
    main(firstLaunchTimes, notFirstLaunchTimes, apkName)


if __name__ == "__main__":
    thread1 = doInThread(runwatch, d, 0)
    time.sleep(30)
    thread2 = doInThread(inputListener, d, 0)
    # 加上下面两行
    settings._init()
    settings.set_value("ffmpeg", 30)
    main(sys.argv[1], sys.argv[2], sys.argv[3])

    # os.system("adb shell input swipe 633 1448 634 1448 10")

# 问题：多设备连接
