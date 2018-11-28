# coding=utf-8
from PIL import Image
import base_utils


# 计算图片的rgb均值
from config.configs import Config
from log.log import MLog


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

    mean_r /= (width * height)
    mean_g /= (width * height)
    mean_b /= (width * height)
    # print "mean: r = {}, g = {}, b = {}".format(mean_r, mean_g, mean_b)
    return mean_r, mean_g, mean_b


def calculate_repos_rgb():
    conf = Config("apk.ini")
    conf_default = Config("default.ini")
    app_key = conf_default.getconf("default").app
    real_homepage = conf.getconf(app_key).homepage
    # homepage_dir = conf.getconf(real_homepage).feature
    path = "./picrepos/homepage/" + real_homepage + "/"
    mean_r = 0
    mean_g = 0
    mean_b = 0
    length_file = base_utils.count_file("picrepos/homepage/" + real_homepage)
    for i in range(1, length_file+1):
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
    if rgb_pic[0] > rgb_folder[0] + 20:
        if rgb_pic[1] > rgb_folder[1] + 20:
            if rgb_pic[2] > rgb_folder[2] + 20:
                return False
    return True


if __name__ == '__main__':
    # calculate_repos_rgb("homepage")
    calculate_pic_rgb("./extract_folder_all/116.jpg")
