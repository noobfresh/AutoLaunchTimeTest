# -*- coding: UTF-8 -*-

import os
import subprocess
import time
import shutil
import threading
import re
from uiautomator import device as d

# 解决即使把adb加入到了path，python也调不到的问题（为了使用UIAutomator引入的）
os.environ.__delitem__('ANDROID_HOME')
os.environ.__setitem__('ANDROID_HOME', 'C:/Users/Administrator/AppData/Local/Android/Sdk/')
os.environ.update()

# 常量初始化
apkName = 'yy.apk'
packageName = 'com.duowan.mobile'
save_dir = '/sdcard/screenrecord/'
# 这个要换成设备名称
temp_dir = 'yy'


# 拿设备信息防止文件夹重名
def getDeviceInfo():
    deviceName = os.popen('adb shell getprop ro.product.model').read()
    global temp_dir
    temp_dir = checkNameValid(deviceName.strip('\n'))
    print deviceName
    return deviceName


# 安装应用
def installAPK(name):
    path = os.path.abspath('.')
    os.chdir(path)
    print path
    os.system("adb install " + name)
    print u'安装成功'


# 授权
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
def screenRecord(name):
    subprocess.Popen("adb shell screenrecord --time-limit 30 " + save_dir + name)
    print u'录屏开始'


# 数据上传
def pullRecord(name):
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
def startAPP():
    # os.system('adb shell monkey -p '+packageName+' -c android.intent.category.LAUNCHER 1')
    d(text='YY').click()
    print u'启动应用'


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


# 注册一些点击事件
def registerEvent(d):
    d.watcher('allowroot').when(text=u'允许').click(text=u'允许')
    d.watcher('allow').when(text=u'始终允许').click(text=u'始终允许')
    d.watcher('anzhuang').when(text=u'继续安装').click(text=u'继续安装')
    d.watcher('az').when(text=u'安装').click(text=u'安装')
    d.watcher('complete').when(text=u'完成').click(text=u'完成')


# 视频转换成帧
# ffmpeg没有视频切成帧输出到指定目录的命令，只能反复调工作目录
def videoToPhoto(dirname, index):
    curPath = os.getcwd()
    print curPath
    if os.path.isdir(dirname):
        os.removedirs(dirname)
    os.makedirs(dirname)
    chagePath = curPath + '/' + dirname
    print chagePath
    os.chdir(chagePath)
    strcmd = 'ffmpeg -i ' + curPath + '\\' + index + '.mp4' + ' -r 60 -f ' + 'image2 %05d.jpg'
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
        time.sleep(0.5)


# main函数，线程sleep时间有待商榷
def main():
    getDeviceInfo()
    print u'输入测试类型: 1->首次启动 2->非首次启动'
    opType = input()
    print u'输入需要测试几次'
    times = input()
    print u'请输入要安装的apk名称：'
    apkName = raw_input()
    installAPK(apkName)
    if opType == 1:
        mkdir(temp_dir)
        for index in range(times):
            clearData()
            time.sleep(3)
            screenRecord(temp_dir + '/' + str(index) + '.mp4')
            time.sleep(3)
            startAPP()
            time.sleep(20)
    elif opType == 2:
        mkdir(temp_dir)
        for index in range(times):
            """
            grantPermission()
            time.sleep(2)
            """
            killProcess()
            time.sleep(2)
            screenRecord(temp_dir + '/' + str(index) + '.mp4')
            time.sleep(3)
            startAPP()
            time.sleep(20)
    time.sleep(30)
    pullRecord(temp_dir)
    path = os.path.abspath('.')
    folder = path + '/' + temp_dir
    print folder
    os.chdir(folder)
    killProcess()
    for index in range(times):
        videoToPhoto(str(temp_dir + "_" + str(index)), str(index))


def start_python():
    doInThread(runwatch, d, 0)
    main()


if __name__ == "__main__":
    doInThread(runwatch, d, 0)
    main()

# 问题：多设备连接




