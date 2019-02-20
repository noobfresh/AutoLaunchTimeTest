# ecoding=utf-8

# 检测目录是否存在，不存在就创建一个
import os
from log.log import MLog


def checkSrcVialdAndAutoCreate(file_path):
    try:
        if not os.path.exists(file_path):
            MLog.debug(u"fileUtil checkSrcVialdAndAutoCreate: 文件路径不存在，现在创建一个...")
            os.makedirs(file_path)
            MLog.debug(u"fileUtil checkSrcVialdAndAutoCreate: 路径为：" + file_path)
    except IOError, e:
        MLog.error(u"fileUtil checkSrcVialdAndAutoCreate: 创建文件失败！，异常如下:")
        MLog.error(u"fileUtil checkSrcVialdAndAutoCreate:: e = " + repr(e))


def fileExist(file):
    if not os.path.exists(file):
        MLog.error(u"fileUtil fileExist: file or src not exist! file = " + file)
        return False
    return True

def count_file(folder, suffix):
    length = []
    for name in os.listdir(folder):
        if name.endswith(suffix):
            length.append(name)
    # MLog.debug(u"fileUtil count_file: folder = " + folder + u" , contain json file size = " + str(len(length)))
    return len(length)
