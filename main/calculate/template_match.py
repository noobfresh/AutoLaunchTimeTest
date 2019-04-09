# coding=utf-8
import datetime

import cv2
import numpy as np

import settings
from calculate.clip import clip_specific_pic, clip_specific_area
from calculate.rgb import calcule_specific_area_rgb
from config.configs import Config
from log.log import MLog
from PIL import Image

from matplotlib import pyplot as plt


def match_img(img, target_img, values, match_path):
    # print img
    # print target_img
    # print match_path
    # 加载原始RGB
    img_rgb = cv2.imread(img)
    # 创建一个原始图像的灰度版本，所有操作在灰度版本中处理，然后在RGB图像中使用相同坐标还原
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    # 加载将要搜索的图像模板
    template = cv2.imread(target_img, 0)
    # 记录图像模板的尺寸，失败原因可能这个图片太大了
    w, h = template.shape[::-1]
    # 使用matchTemplate对原始灰度图像和图像模板进行匹配（调接口，这个值可以打印一下，不知道是个什么值）
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)  # 最后这个参数可以试一下调一下
    # print "what! there is a result = {}".format(res)
    # 根据外部传参设置阈值
    threshold = values
    # print res >= threshold
    loc = np.where(res >= threshold)

    x = 0
    y = 0
    # 匹配完成后在原始图像中使用灰度图像的坐标对原始图像进行标记。
    mflag = False
    for pt in zip(*loc[::-1]):
        x = pt[0]
        y = pt[1]
        if x != 0 and y != 0 and not mflag:
            mflag = True
            feature = img_rgb[y:y + h, x:x + w]
            # 首帧多了很多遍操作。减少到1次
            cv2.imwrite(match_path, feature)
            MLog.debug("match_img: clip picture success path = " + img)
        # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 10)  # 有一个是rgb, 最后这个和画笔粗细有关

    # 写下来
    # cv2.imwrite('./extract_folder_all/' + name + '_copy.jpg', img_rgb)
    # print "i have written it down"


# 提供vivoX9 找不到启动坐标使用
def findLaunchLogo(src_path, dst_path):
    # 加载原始RGB
    img_rgb = cv2.imread(src_path)
    # 创建一个原始图像的灰度版本，所有操作在灰度版本中处理，然后在RGB图像中使用相同坐标还原
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    # 加载将要搜索的图像模板
    template = cv2.imread(dst_path, 0)
    # 记录图像模板的尺寸，失败原因可能这个图片太大了
    w, h = template.shape[::-1]
    # 使用matchTemplate对原始灰度图像和图像模板进行匹配（调接口，这个值可以打印一下，不知道是个什么值）
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)  # 最后这个参数可以试一下调一下
    # print "what! there is a result = {}".format(res)
    # 根据外部传参设置阈值
    threshold = 0.95
    # print res >= threshold
    loc = np.where(res >= threshold)

    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    # 匹配完成后在原始图像中使用灰度图像的坐标对原始图像进行标记。
    for pt in zip(*loc[::-1]):
        x1 = pt[0]
        y1 = pt[1]
        if x1 != 0 and y1 != 0:
            x2 = x1 + w
            y2 = y1 + h
    position = {'left': x1, 'top': y1, 'right': x2, 'bottom': y2}
    return position


# 专门来判断是否启动完成（启动页是否加载完）
def isLaunchingPage(src, target_path):
    # 加载原始RGB
    img_rgb = cv2.imread(src)
    # 创建一个原始图像的灰度版本，所有操作在灰度版本中处理，然后在RGB图像中使用相同坐标还原
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    # 加载将要搜索的图像模板
    template = cv2.imread(target_path, 0)
    # 记录图像模板的尺寸，失败原因可能这个图片太大了
    w, h = template.shape[::-1]
    # 使用matchTemplate对原始灰度图像和图像模板进行匹配（调接口，这个值可以打印一下，不知道是个什么值）
    res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)  # 最后这个参数可以试一下调一下
    # print "what! there is a result = {}".format(res)
    # 根据外部传参设置阈值
    # print str(float(res)) + " -------------------------------------"
    threshold = 0.9955
    # print res >= threshold
    loc = np.where(res >= threshold)

    # 匹配完成后在原始图像中使用灰度图像的坐标对原始图像进行标记。
    for pt in zip(*loc[::-1]):
        x1 = pt[0]
        y1 = pt[1]
        if x1 != 0 and y1 != 0:
            return True
    return False


def isHomepageFinish(path):
    img = cv2.imread(path)
    height, width, something = img.shape
    # print "width = {}, height = {}, something = {}".format(width, height, something)
    rgb = img[height - 30, 30]
    print rgb
    if rgb[0] >= 253 and rgb[1] >= 253 and rgb[2] >= 253:
        return True
    return False


def test():
    img = cv2.imread("F:\cvtest\\test11.jpg")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gaus = cv2.GaussianBlur(gray, (19, 19), 0)

    ret, binary = cv2.threshold(gaus, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)

    edges = cv2.Canny(binary, 1, 20, apertureSize=3)

    minLineLength = 100
    maxLineGap = 75
    lines = cv2.HoughLinesP(edges, 1, np.pi / 2, 100, minLineLength, maxLineGap)
    # print a + "-------------------"
    # print b + "-------------------"
    # print c + "-------------------"
    print len(lines)
    # for x1, y1, x2, y2 in lines[0]:
    #     cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    for i in range(0, len(lines)):
        for x1, y1, x2, y2 in lines[i]:
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
    cv2.imwrite("F:\cvtest\linedetect.jpg", img)
    cv2.imwrite("F:\cvtest\linedges.jpg", edges)
    # cv2.imwrite("F:\\ret.jpg", ret)
    cv2.imwrite("F:\cvtest\\binary.jpg", binary)


def direct_fuck(path):
    clip_specific_pic(path, "F:\cvtest\\test_clip.jpg")
    img = cv2.imread("F:\cvtest\\test_clip.jpg")
    height, width, something = img.shape
    print "height = {}, width = {}".format(height, width)
    start_time = datetime.datetime.now()
    y_array = [0]
    array_flag = False
    for i in range(0, height, 2):
        # 行数遍历
        count = 0
        for j in range(0, width, 1):
            if img[i, j][0] >= 252 and img[i, j][1] >= 252 and img[i, j][2] >= 252:
                count += 1
        if count >= width / 2:
            # print count
            if not array_flag:
                y_array.append(i)
                array_flag = True
            for j in range(width):
                img[i, j] = [255, 255, 255]
        else:
            if array_flag:
                y_array.append(i - 1)
                array_flag = False
            for j in range(width):
                img[i, j] = [0, 0, 0]
    cv2.imwrite("F:\cvtest\\detect.jpg", img)
    # 前面这个计算时间太长了
    print "pre-deal time = {}".format(datetime.datetime.now() - start_time)
    test_count = 0
    print y_array
    for t in range(1, len(y_array)):
        if y_array[t] - y_array[t-1] > 120:
            # 测试过程可以打开这个
            clip_specific_area("F:\cvtest\\test_clip.jpg", "F:\cvtest\\" + str(test_count) + ".jpg",
                               0, y_array[t-1], width/2, y_array[t])
            test_count += 1
            mean_r, mean_g, mean_b = calcule_specific_area_rgb("F:\cvtest\\test_clip.jpg",
                                                               0, y_array[t-1], width/2, y_array[t])
            gray_range = range(231, 241)
            if mean_r in gray_range and mean_g in gray_range and mean_r in gray_range:
                return False

            clip_specific_area("F:\cvtest\\test_clip.jpg", "F:\cvtest\\" + str(test_count) + ".jpg",
                               width / 2, y_array[t - 1], width, y_array[t])
            test_count += 1

            mean_r, mean_g, mean_b = calcule_specific_area_rgb("F:\cvtest\\test_clip.jpg",
                                                               width/2, y_array[t-1], width, y_array[t])
            if mean_r in gray_range and mean_g in gray_range and mean_r in gray_range:
                return False

    # 取出来了3个块，第一步先不做竖直线的查找，先直接对半分计算一下每个块的rgb,两个方案 ->
    # 一个是直接算切出来的方块的平均rgb，另一个就算238238238附近的像素点能达到这个方块的百分之50吗
    print "all time = {}".format(datetime.datetime.now() - start_time)
    return True


def isHomePageLoadFinish(path, dstPath):
    clip_specific_pic(path, dstPath)
    img = cv2.imread(dstPath)
    height, width, something = img.shape
    print "height = {}, width = {}".format(height, width)
    # print len(dstPath)
    # print dstPath[0: len(dstPath) - 4]
    start_time = datetime.datetime.now()
    y_array = [0]
    array_flag = False
    for i in range(0, height, 2):
        # 行数遍历
        count = 0
        for j in range(0, width, 1):
            if img[i, j][0] >= 252 and img[i, j][1] >= 252 and img[i, j][2] >= 252:
                count += 1
        if count >= width / 2:
            # print count
            if not array_flag:
                y_array.append(i)
                array_flag = True
            for j in range(width):
                img[i, j] = [255, 255, 255]
        else:
            if array_flag:
                y_array.append(i - 1)
                array_flag = False
            for j in range(width):
                img[i, j] = [0, 0, 0]
    # cv2.imwrite("F:\cvtest\\detect.jpg", img)
    # 前面这个计算时间太长了
    print "pre-deal time = {}".format(datetime.datetime.now() - start_time)
    test_count = 0
    print y_array
    for t in range(1, len(y_array)):
        if y_array[t] - y_array[t - 1] > 120:
            # 测试过程可以打开这个
            # clip_specific_area(dstPath, dstPath[0, len(dstPath) - 4] + str(test_count) + ".jpg",
            #                    0, y_array[t - 1], width / 2, y_array[t])
            test_count += 1
            mean_r, mean_g, mean_b = calcule_specific_area_rgb(dstPath,
                                                               0, y_array[t - 1], width / 2, y_array[t])
            gray_range = range(231, 241)
            if mean_r in gray_range and mean_g in gray_range and mean_r in gray_range:
                return False

            # clip_specific_area(dstPath, dstPath[0, len(dstPath) - 4] + str(test_count) + ".jpg",
            #                    width / 2, y_array[t - 1], width, y_array[t])
            test_count += 1

            mean_r, mean_g, mean_b = calcule_specific_area_rgb(dstPath,
                                                               width / 2, y_array[t - 1], width, y_array[t])
            if mean_r in gray_range and mean_g in gray_range and mean_r in gray_range:
                return False

    # 取出来了3个块，第一步先不做竖直线的查找，先直接对半分计算一下每个块的rgb,两个方案 ->
    # 一个是直接算切出来的方块的平均rgb，另一个就算238238238附近的像素点能达到这个方块的百分之50吗
    print "all time = {}".format(datetime.datetime.now() - start_time)
    return True


def get_ent_pos(path, out_path, machineName):
    origin_height = clip_specific_pic(path, out_path + machineName + "_clip.jpg")
    img = cv2.imread(out_path + machineName + "_clip.jpg")
    height, width, something = img.shape
    print "height = {}, width = {}".format(height, width)
    start_time = datetime.datetime.now()
    y_array = [0]
    array_flag = False
    for i in range(0, height, 2):
        # 行数遍历
        count = 0
        for j in range(0, width, 2):
            if img[i, j][0] >= 252 and img[i, j][1] >= 252 and img[i, j][2] >= 252:
                count += 1
        if count >= width / 4:
            # print count
            if not array_flag:
                y_array.append(i)
                array_flag = True
        else:
            if array_flag:
                y_array.append(i - 1)
                array_flag = False
    print "pre-deal time = {}".format(datetime.datetime.now() - start_time)
    print y_array
    ent_part_pair = []
    for t in range(1, len(y_array)):
        if y_array[t] - y_array[t-1] > 120:
            # 测试过程可以打开这个
            ent_part_pair.append((y_array[t-1], y_array[t]))
    print ent_part_pair
    print "all time = {}".format(datetime.datetime.now() - start_time)
    x = width*3/4
    leng_arr = len(ent_part_pair)
    # 特征直播间存起来，似乎不用裁剪，只要专门往上算10个px（有坐标就行），看这10个px平均RGB多少，拿什么存坐标呢（settings）
    # 还是要裁剪图片的，因为需要图片来判断是否进入直播间成功
    # 裁第几格子，这个要靠app判断，读配置文件
    conf_default = Config("default.ini")
    app_key = conf_default.getconf("default").app
    count = 2
    if app_key == "bigo":
        count = 1
    clip_specific_area(out_path + machineName + "_clip.jpg", out_path + machineName + "_feature.jpg",
                       width/4, ent_part_pair[leng_arr-count][0],
                       width, ent_part_pair[leng_arr-count][1])
    settings.set_value("feature_path", out_path + machineName + "_feature.jpg")
    settings.set_value("ent_top_pos_x", x)
    settings.set_value("ent_top_pos_y", ent_part_pair[leng_arr-count][0] + origin_height*0.12)
    # 潜规则，要加上12%的高度，因为裁图裁掉了12%
    y = (ent_part_pair[leng_arr-count][0] + ent_part_pair[leng_arr-count][1])/2 + origin_height*0.12
    print "finally x = {}, y = {}".format(x, y)
    return x, y


def test1():
    # 做直线识别测试
    print 1
    im = Image.open("F:\\360WiFi\\3.jpg")
    pix = im.load()
    width = im.size[0]
    height = im.size[1]
    print "width = {}, height = {}".format(width, height)
    count = 0
    for i in range(width):
        for j in range(height):
            r, g, b = pix[i, j]
            if r <= 50 and g <= 50 and b <= 50:
                count += 1
        if count > height*2/3:
            return i
    return -1


def test2():
    img = cv2.imread("F:\\360WiFi\\00114.jpg")
    img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()
    print imageVar


if __name__ == '__main__':
    # isHomepageFinish("F:\\test2.jpg")
    # test()
    # print findLaunchLogo("F:\\test2.jpg", "F:\\feature.jpg")
    # print get_ent_pos("F:\cvtest\\test39.jpg")
    print isHomePageLoadFinish("F:\cvtest\\test31.jpg", "F:\cvtest\\test00.jpg")
    # clip_specific_area("F:\github\main\screenrecord\MI8_enterliveroom\MI8_enterliveroom_0\\00114.jpg",
    #                    "F:\\360WiFi\\00114.jpg", 810, 240, 1080, 780)
    # test2()

    print 1

