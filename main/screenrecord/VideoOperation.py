# -*- coding: UTF-8 -*-
from screenrecord.BaseConfig import BaseConfig
import os
import time
import shutil
import subprocess
from log.log import MLog
from screenrecord.DeviceInfo import DeviceInfo


class VideoOperation(BaseConfig):

    def __init__(self, sernum):
        super(VideoOperation, self).__init__()
        self.saveDir = '/sdcard/screenrecord/'
        self.serNum = sernum
        self.device = DeviceInfo(sernum)
        self.machineName = self.device.getDeviceInfo()

    # 录屏
    def screenRecord(self, d, times, name):
        if self.machineName == "PACM00":
            os.system('adb -s ' + self.serNum + ' shell service call statusbar 1')
            d(text="开始录屏").click()
            print "start"
            time.sleep(5)
        else:
            print(name + "         ----------------------------------                ---------------------------")
            subprocess.Popen("adb -s " + self.serNum + " shell screenrecord --bit-rate 10000000 --time-limit " + str(
                times) + " " + self.saveDir + name)
            time.sleep(2)
        MLog.info(u"video_operation screenRecord: 录屏开始")

    # 数据上传
    def pullRecord(self, name):
        curPath = os.getcwd()
        if self.machineName == "PACM00":
            os.system("adb -s " + self.serNum + "  pull " + name)
        else:
            os.system("adb -s " + self.serNum + "  pull " + self.saveDir + name)
            MLog.info(u"video_operation pullRecord: 数据上传成功")
            path = os.path.dirname(__file__) + "\\"
            srcPath = os.path.join(os.path.dirname(path), name)
            print srcPath + "pull record----"
            os.chdir(srcPath)
            for root, dirs, files in os.walk(srcPath):  # 遍历统计
                for file in files:
                    if file.__contains__('_'):
                        os.rename(file, file.split('_')[0] + ".mp4")
            os.chdir(curPath)

    # 视频转换成帧
    # ffmpeg没有视频切成帧输出到指定目录的命令，只能反复调工作目录
    def videoToPhoto(self, dirname, index):
        curPath = os.getcwd()

        if self.machineName == "PACM00":
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
            os.chdir(curPath)

        MLog.info(u"video_operation videoToPhoto:" + '+++++++++++++' + curPath)
        if os.path.isdir(dirname):
            shutil.rmtree(dirname)
        os.makedirs(dirname)
        chagePath = curPath + '/' + dirname
        print '+++++++++++++' + chagePath
        os.chdir(chagePath)
        strcmd = 'ffmpeg -i ' + curPath + '/' + index + '.mp4' + ' -r ' + str(50) + ' -f ' + 'image2 %05d.jpg'
        subprocess.call(strcmd, shell=True)
        os.chdir(curPath)
