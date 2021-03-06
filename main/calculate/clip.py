# coding=utf-8
import cv2

from PIL import Image
import os
import base_utils
from log.log import MLog


def clip(path, count):
    for i in range(1, count + 1):
        complete_path = path + base_utils.adapter_num(i) + ".jpg"
        MLog.debug("clip(): the complete path = {}".format(complete_path))
        img = Image.open(complete_path)
        width = img.size[0]
        height = img.size[1]
        img = img.crop(
            (
                0,
                300,
                width,
                height - 200
            )
        )
        # os.remove(path)
        img.save(base_utils.rename_path(path, i))
        # print base_utils.rename_path(path, i)


def clip_specific_pic(path, dst_path):
    if path.find(".png") != -1:
        img = cv2.imread(path)
        # 防png
        path = path.replace(".png", ".jpg")
        cv2.imwrite(path, img)
    MLog.debug("clip_specific_pic(): the path = {}".format(path))
    img = Image.open(path)
    # img.convert("RGB")
    # img.save("F:\\cao.jpg")
    width = img.size[0]
    height = img.size[1]
    # 上面部分裁剪 12%， 下面部分裁剪0%
    top_margin = int(height * 0.12)
    bottom_margin = int(height * 0)
    img = img.crop(
        (
            0,
            top_margin,
            width,
            height - bottom_margin
        )
    )
    img.save(dst_path)
    return height


def clip_generate_flag(path1, path2):
    MLog.debug("clip_specific_pic(): the path = {}".format(path1))
    img = Image.open(path1)
    width = img.size[0]
    height = img.size[1]
    img = img.crop(
        (
            0,
            300,
            width,
            height - 200
        )
    )
    img.save(path2)


def clip_specific_area(src, dst, x1, y1, x2, y2):
    img = Image.open(src)
    img = img.crop(
        (
            x1,
            y1,
            x2,
            y2
        )
    )
    img.save(dst)


def clip_half_pic(path):
    img = Image.open(path)
    width = img.size[0]
    height = img.size[1]
    img = img.crop(
        (
            width/2,
            0,
            width,
            height
        )
    )
    img.save(path)


if __name__ == '__main__':
    clip_specific_pic("../screenrecord/MI8_first/MI8_first_0/00475.jpg")
    print 1