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


def clip_specific_pic(path):
    MLog.debug("clip_specific_pic(): the path = {}".format(path))
    img = Image.open(path)
    width = img.size[0]
    height = img.size[1]
    img = img.crop(
        (
            0,
            400,
            width,
            height - 350
        )
    )
    img.save(path)


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


if __name__ == '__main__':
    clip_specific_pic("../screenrecord/MI8_first/MI8_first_0/00475.jpg")
    print 1