# coding=utf-8
import cv2
import os

import base_utils
from log.log import MLog
from template_match import match_img
from color_histogram import calculate_by_hists
from PIL import Image

first_frame_feature = "./feature/vivoX7_launch_feature.jpg"  # 配置项
threshold = 0.95
base_path = "./extract_folder_all/"


# 首帧计算过程
def first_frame_find(length, real_path, real_feature_path):
    for i in range(1, length+1):
        src_file_path = real_path + base_utils.adapter_num(i) + ".jpg"
        feature_name = real_path + base_utils.adapter_num(i) + "_feature.jpg"
        # print src_file_path
        # print real_feature_path
        match_img(src_file_path, real_feature_path, threshold, feature_name)
        if base_utils.os.path.exists(feature_name):
            # 首帧思路，如果识别到了，取出截取部分与特征图做个彩色直方图对比，确定
            degree = calculate_by_hists(real_feature_path, feature_name)
            # print degree
            if degree > 0.6:
                return i
        MLog.debug("first_frame_find: " + src_file_path + " is not first frame")
    return -1


def new_first_frame_find(start_index, length, real_path, real_feature_path):
    for i in range(start_index, length+1):
        src_file_path = real_path + base_utils.adapter_num(i) + ".jpg"
        feature_name = real_path + base_utils.adapter_num(i) + "_feature.jpg"
        # print src_file_path
        # print real_feature_path
        match_img(src_file_path, real_feature_path, threshold, feature_name)
        if base_utils.os.path.exists(feature_name):
            # 首帧思路，如果识别到了，取出截取部分与特征图做个彩色直方图对比，确定
            degree = calculate_by_hists(real_feature_path, feature_name)
            # print degree
            if degree > 0.6:
                return i
        MLog.debug("new_first_frame_find: " + src_file_path + " is not first frame")
    return -1


def enter_ent_first_frame_find(file_count, path, x, y):
    print "enter_ent_first_frame_find, file_count = {}, path = {}, x = {}, y = {}".format(file_count, path, x, y)
    for i in range(1, file_count):
        # print os.getcwd()
        src_file_path = path + base_utils.adapter_num(i) + ".jpg"
        print src_file_path
        img = Image.open(src_file_path)
        pix = img.load()
        x = int(x)
        y = int(y)
        mean_r = 0
        mean_g = 0
        mean_b = 0
        for j in range(1, 11):
            # r, g, b =
            # print y-j
            # print "r = {}, g = {}, b = {}".format(pix[x, y-j][0], pix[x, y-j][1], pix[x, y-j][2])
            mean_r += pix[x, y-j][0]
            mean_g += pix[x, y-j][1]
            mean_b += pix[x, y-j][2]
        mean_r /= 10
        mean_g /= 10
        mean_b /= 10
        print u"index = {},传说中的向上10个px的像素的点的RGB = {}, {}, {}".format(i, mean_r, mean_g, mean_b)
        if mean_r < 250 and mean_g < 250 and mean_b < 250:
            return i
    return -1


def test():
    path = "../screenrecord/Mi8_enterliveroom/00001.jpg"
    x = 810
    y = 823
    mean_r = 0
    mean_g = 0
    mean_b = 0
    # img = Image.open(path)
    # pix = img.load()
    img = cv2.imread(path)
    for j in range(1, 11):
        # r, g, b =
        print y - j
        print "r = {}, g = {}, b = {}".format(img[y - j, x][0], img[y - j, x][1], img[y - j, x][2])
        # img[y - j, x][0] = 0
        # img[y - j, x][1] = 255
        # img[y - j, x][2] = 255
        mean_r += img[y - j, x][0]
        mean_g += img[y - j, x][1]
        mean_b += img[y - j, x][2]
    mean_r /= 10
    mean_g /= 10
    mean_b /= 10
    # cv2.imwrite("../screenrecord/Mi8_enterliveroom/00001_test.jpg", img)
    # img.save("../screenrecord/Mi8_enterliveroom/00001_test.jpg")
    print u"index = {},传说中的向上10个px的像素的点的RGB = {}, {}, {}".format(1, mean_r, mean_g, mean_b)


if __name__ == '__main__':
    # index = first_frame_find()
    # if index > 0:
    #     print "the first frame index = {}".format(index)
    # else:
    #     print "i have not found first frame"
    # enter_ent_first_frame_find(10, "F:\github\main\screenrecord\MiNote2_enterliveroom\MiNote2_enterliveroom_0\\", 810, 837)
    test()
