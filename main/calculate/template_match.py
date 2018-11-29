# coding=utf-8

import cv2
import numpy as np
from PIL import Image

from base_utils import rename_path
from log.log import MLog


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


if __name__ == '__main__':
    image = "../screen.jpg"
    target = "../feature/vivoX9_launch_feature.jpg"
    value = 0.9
    match_img(image, target, value, "aaaaaaaaaa.jpg")

