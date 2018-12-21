#!/usr/bin/python
# coding=utf-8
import os
import time
from zipfile import *

from log import MLog


def get_items_list_in_dir(src, lst):
    for item in os.listdir(src):
        path = os.path.join(src, item)
        if os.path.splitext(path)[1] == '.txt':
            lst.append(path)
            # print "add " + path

        # if os.path.isdir(path):
        #     get_items_list_in_dir(path, lst)


def make_patch(dir_input, file_output):
    MLog.debug(u"输入地址: " + dir_input)
    MLog.debug(u"输出地址: " + file_output)
    itemList = []
    get_items_list_in_dir(dir_input, itemList)
    with ZipFile(file_output, 'w', ZIP_DEFLATED) as myzip:
        for item in itemList:
            new_item = item
            new_item = new_item.split(os.sep)[-1]
            print "%s ==> %s" % (item, new_item)
            myzip.write(item, new_item)


def make_log_patch():
    file_path = os.path.dirname(__file__) + os.sep + "files"
    suffix = '.zip'
    prefix = "log"
    file_output = file_path + os.sep + prefix + time.strftime("_%Y_%m_%d") + suffix
    make_patch(file_path, file_output)
    return file_output


if __name__ == '__main__':
    make_log_patch()
