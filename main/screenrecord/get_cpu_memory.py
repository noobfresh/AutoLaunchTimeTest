# coding=utf-8
import os
import threading

from log.log import MLog

pkg_name = "com.duowan"


def get_mem_cpu():
    r = os.popen("adb shell top -n 1")
    text = r.read()
    r.close()
    MLog.info(text[0:1000])


if __name__ == '__main__':
    get_mem_cpu()
