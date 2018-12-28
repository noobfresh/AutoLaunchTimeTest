# coding=utf-8
from PIL import Image
import base_utils

# 计算图片的rgb均值
from config.configs import Config
from log.log import MLog

conf = Config("default.ini")
feature_path = conf.getconf("default").feature_path


def calculate_pic_rgb(path):
    im = Image.open(path)
    pix = im.load()
    width = im.size[0]
    height = im.size[1]
    mean_r = 0
    mean_g = 0
    mean_b = 0
    for x in range(width):
        for y in range(height):
            r, g, b = pix[x, y]
            mean_r += r
            mean_g += g
            mean_b += b
            # print "r = {}, g = {}, b = {}".format(r, g, b)

    mean_r /= (width * height)
    mean_g /= (width * height)
    mean_b /= (width * height)
    # MLog.debug("mean: r = {}, g = {}, b = {}".format(mean_r, mean_g, mean_b))
    return mean_r, mean_g, mean_b


def calculate_repos_rgb():
    conf = Config("apk.ini")
    conf_default = Config("default.ini")
    app_key = conf_default.getconf("default").app
    real_homepage = conf.getconf(app_key).homepage
    # homepage_dir = conf.getconf(real_homepage).feature
    path = feature_path + "/picrepos/homepage/" + real_homepage + "/"
    mean_r = 0
    mean_g = 0
    mean_b = 0
    length_file = base_utils.count_file(feature_path + "/picrepos/homepage/" + real_homepage)
    for i in range(1, length_file + 1):
        rgb = calculate_pic_rgb(path + base_utils.adapter_num(i) + ".jpg")
        mean_r += rgb[0]
        mean_g += rgb[1]
        mean_b += rgb[2]
    mean_r /= length_file
    mean_g /= length_file
    mean_b /= length_file
    MLog.debug("calculate_repos_rgb: the folder mean rgb: r = {}, g = {}, b = {}".format(mean_r, mean_g, mean_b))
    return mean_r, mean_g, mean_b


def calculate_homepage_rgb():
    rgb_folder = calculate_repos_rgb()
    return rgb_folder


def compare_rgb(path, rgb_folder):
    rgb_pic = calculate_pic_rgb(path)
    # 主要就是怎么比这几个值了，要根据哪个值为准呢
    # 当前我决定取，rgb每个值都差了15 以上，则认为还没加载完成，这个值取啥一样是个难点
    r_threshold = 20
    g_threshold = 20
    b_threshold = 20
    conf_default = Config("default.ini")
    app_key = conf_default.getconf("default").app
    # 陌陌由于白色部分过于多，因此把上限范围弄小点
    if app_key == "momo":
        r_threshold = 10
        g_threshold = 10
        b_threshold = 10

    # 除了上限，还要加个下限，预防启动黑了的情况
    if rgb_pic[0] > rgb_folder[0] + r_threshold:
        if rgb_pic[1] > rgb_folder[1] + g_threshold:
            if rgb_pic[2] > rgb_folder[2] + b_threshold:
                return False
    if rgb_pic[0] < rgb_folder[0] - 50:
        if rgb_pic[1] < rgb_folder[1] - 50:
            if rgb_pic[2] < rgb_folder[2] - 50:
                return False
    return True


def test(path):
    im = Image.open(path)
    pix = im.load()
    width = im.size[0]
    height = im.size[1]
    # 想办法如何 以 滑动窗口的形式计算 窗口大小50*50
    count = 0
    just_count = 0
    for x in range(0, width / 25):
        for y in range(0, height / 25):
            # 继续for
            start_x = x * 25
            start_y = y * 25
            mean_r = 0
            mean_g = 0
            mean_b = 0
            for temp_x in range(start_x, start_x + 25):
                for temp_y in range(start_y, start_y + 25):
                    r, g, b = pix[x, y]
                    mean_r += r
                    mean_g += g
                    mean_b += b
            mean_r /= 625
            mean_g /= 625
            mean_b /= 625
            just_count += 1
            print "r = {}, g = {}, b = {}".format(mean_r, mean_g, mean_b)
            if mean_r == 238 and mean_g == 238 and mean_b == 238:
                count += 1
    print count
    print just_count


def calcule_specific_area_rgb(path, x1, y1, x2, y2):
    im = Image.open(path)
    pix = im.load()
    mean_r = 0
    mean_g = 0
    mean_b = 0
    for i in range(x1, x2):
        for j in range(y1, y2):
            mean_r += pix[i, j][0]
            mean_g += pix[i, j][1]
            mean_b += pix[i, j][2]
    pixles = (x2 - x1) * (y2 - y1)
    mean_r /= pixles
    mean_g /= pixles
    mean_b /= pixles
    MLog.debug("mean: r = {}, g = {}, b = {}".format(mean_r, mean_g, mean_b))
    return mean_r, mean_g, mean_b


if __name__ == '__main__':
    print calculate_pic_rgb("F:\\photo2.jpg")
    # test("F:\\test3.jpg")
