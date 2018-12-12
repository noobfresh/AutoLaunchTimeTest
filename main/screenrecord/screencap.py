# -*- coding: UTF-8 -*-
import os
import subprocess

out_path = os.path.dirname(__file__) + os.sep + "cap.jpg"


class Screenshot():  # 截取手机屏幕并保存到电脑
    def __init__(self):
        # 查看连接的手机
        connect = subprocess.Popen("adb devices", stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        stdout, stderr = connect.communicate()  # 获取返回命令
        # 输出执行命令结果结果
        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")
        print(stdout)
        print(stderr)

    def screen(self, cmd):  # 在手机上截图
        screenExecute = subprocess.Popen(str(cmd), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        stdout, stderr = screenExecute.communicate()
        # 输出执行命令结果结果
        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")
        print(stdout)
        print(stderr)

    def saveComputer(self, cmd):  # 将截图保存到电脑
        screenExecute = subprocess.Popen(str(cmd), stderr=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
        stdout, stderr = screenExecute.communicate()
        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")
        # 输出执行命令结果结果
        stdout = stdout.decode("utf-8")
        stderr = stderr.decode("utf-8")
        print(stdout)
        print(stderr)


def cap(sernum):
    img_name = sernum + "_cap.jpg"
    cmd1 = r"adb -s " + sernum + " shell /system/bin/screencap -p /sdcard/" + img_name  # 命令1：在手机上截图cap.png为图片名
    # cmd2 = r"adb pull /sdcard/cap.png ."  # 命令2：将图片保存到电脑
    cmd2 = r"adb -s " + sernum + " pull /sdcard/" + img_name + " " + out_path
    screen = Screenshot()
    screen.screen(cmd1)
    screen.saveComputer(cmd2)
    return out_path


if __name__ == '__main__':
    cap()
