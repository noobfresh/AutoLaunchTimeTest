# coding=utf-8
import os

import cv2
from PIL import Image
from skimage.measure import compare_mse
from skimage.measure import compare_psnr
from skimage.measure import compare_ssim
import numpy as np
from compiler.ast import flatten
import math
import operator

from base_utils import adapter_num


def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        image = cv2.imread(os.path.join(folder, filename))
        if image is not None:
            images.append(image)
    return images


def to_gray(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# PHash算法
def pHash(imgfile):
    """get image pHash value"""
    # 加载并调整图片为32x32灰度图片
    img = cv2.imread(imgfile, 0)
    img = cv2.resize(img, (64, 64), interpolation=cv2.INTER_CUBIC)

    # 创建二维列表
    h, w = img.shape[:2]
    vis0 = np.zeros((h, w), np.float32)
    vis0[:h, :w] = img  # 填充数据

    # 二维Dct变换
    vis1 = cv2.dct(cv2.dct(vis0))
    # cv.SaveImage('a.jpg',cv.fromarray(vis0)) #保存图片
    vis1.resize(32, 32)

    # 把二维list变成一维list
    img_list = flatten(vis1.tolist())

    # 计算均值
    avg = sum(img_list) * 1. / len(img_list)
    avg_list = ['0' if i < avg else '1' for i in img_list]

    # 得到哈希值
    return ''.join(['%x' % int(''.join(avg_list[x:x + 4]), 2) for x in range(0, 32 * 32, 4)])


# 汉明距离
def hammingDist(s1, s2):
    assert len(s1) == len(s2)
    return sum([ch1 != ch2 for ch1, ch2 in zip(s1, s2)])


# 均衡直方图
def compare(pic1, pic2):

    image1 = Image.open(pic1)
    image2 = Image.open(pic2)

    histogram1 = image1.histogram()
    histogram2 = image2.histogram()

    differ = math.sqrt(reduce(operator.add, list(map(lambda a, b: (a-b)**2, histogram1, histogram2)))/len(histogram1))

    return differ


def phashfinal(path1, path2):
    img1 = path1
    img2 = path2
    hash1 = pHash(img1)
    hash2 = pHash(img2)
    out_score1 = 1 - hammingDist(hash1, hash2) * 1. / (32 * 32 / 4)
    return out_score1


def psnr(path1, path2):
    img1 = cv2.imread(path1)
    img2 = cv2.imread(path2)
    psnr = compare_psnr(img1, img2)
    return psnr


# 所谓入口
if __name__ == '__main__':
    basePath = "./extract_folder/"
    targetimages = load_images_from_folder(basePath)
    # listLine = []
    listLine2 = []
    for i in range(1, len(targetimages)-1):
        # mse = compare_mse(targetimages[i], targetimages[i + 1])
        # psnr = compare_psnr(targetimages[i], targetimages[i + 1])
        ssim = compare_ssim(to_gray(targetimages[i]), to_gray(targetimages[i + 1]))
        # histogram = compare(renamePath(i), renamePath(i+1))
        # pHashAns = phashfinal(i, i+1)
        print ("------------id: {}~{}".format(i, i+1))
        # print ("MSE: {}".format(mse))
        # print ("PSNR: {}".format(psnr))
        print ("SSIM: {}".format(ssim))
        # print ("histogram: {}".format(histogram))
        # print ("PHASH: {}".format(pHashAns))
        # listLine.append(pHashAns)
        listLine2.append(ssim)
    # charts.test(listLine2, len(listLine2))
