# -*- coding: UTF-8 -*-

import os
import time
import shutil
import subprocess
from sub_thread import doInThread

save_dir = '/sdcard/screenrecord/'


# 录屏
def screenRecord(d, times, name, sernum, machineName):
    if machineName == "PACM00":
        os.system('adb -s ' + sernum + ' shell service call statusbar 1')
        d(text="开始录屏").click()
        print "start"
        time.sleep(5)
    else:
        print(name + "         ----------------------------------                ---------------------------")
        subprocess.Popen("adb -s " + sernum + " shell screenrecord --bit-rate 10000000 --time-limit " + str(
            times) + " " + save_dir + name)
    doInThread(get_mem_cpu, d, 0)
    print u'录屏开始'


# 数据上传
def pullRecord(name, sernum, machineName):
    curPath = os.getcwd()
    if machineName == "PACM00":
        os.system("adb -s " + sernum + "  pull " + name)
    else:
        print save_dir + name
        os.system("adb -s " + sernum + "  pull " + save_dir + name)
        print u'数据上传成功'
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
def videoToPhoto(dirname, index, machineName):
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
    # print u"帧数 = " + str(settings.get_value("ffmpeg"))
    strcmd = 'ffmpeg -i ' + curPath + '/' + index + '.mp4' + ' -r ' + str(50) + ' -f ' + 'image2 %05d.jpg'
    # strcmd = 'ffmpeg -i ' + curPath + '/' + index + '.mp4' + ' -r ' + str(
    #      settings.get_value("ffmpeg")) + ' -f ' + 'image2 %05d.jpg'
    subprocess.call(strcmd, shell=True)
    os.chdir(curPath)


def get_mem_cpu(d, data):
    # for i in range(0, 3):
    #     r = os.popen("adb shell top -n 1")
    #     text = r.read()
    #     r.close()
    #     MLog.info(text[0:1000])
    #     time.sleep(5)
    print 1
