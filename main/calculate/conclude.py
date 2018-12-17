# coding=utf-8
import datetime
from multiprocessing.dummy import Pool as ThreadPool
from os.path import exists

import settings
from base_utils import count_dirs, count_file
from config.configs import Config
from first_frame_calculate import first_frame_find
from last_frame_calculate import last_and_launching_frame_find_rgb, huya_first_find_frame
from log.log import MLog
from rgb import calculate_homepage_rgb

conf = Config("default.ini")
path = conf.getconf("default").feature_path
rgb_folder = calculate_homepage_rgb()  # 计算样本库的rgb均值


# 每个目录算一次，这种计算只针对普通启动： 置灰 -> 启动页 -> 正常首页
def multi_normal_calculate_part(params):
    device_name = params["device"]  # 设备名称
    name_with_suffix = device_name + "_" + params["suffix"]  # 通常suffix = first / notfirst
    dir_index = params["dir_index"]  # 当前算的第几组数据
    # rgb_folder = calculate_homepage_rgb()  # 计算样本库的rgb均值
    conf = Config("apk.ini")
    conf_default = Config("default.ini")
    app_key = conf_default.getconf("default").app
    feature_dir = conf.getconf(app_key).feature  # 特征图的文件夹名字
    file_count = count_file("./screenrecord/" + name_with_suffix + "/" + name_with_suffix + "_" + str(dir_index))
    real_path = "./screenrecord/" + name_with_suffix + "/" + name_with_suffix + "_" + str(dir_index) + "/"
    real_first_feature_path = path + "/picrepos/feature/" + feature_dir + "/" + device_name + "_launch_feature.jpg"
    if not exists(real_first_feature_path):
        MLog.debug("calculate: first, there is no adapted feature pic for current Phone")
        real_first_feature_path = path + "/picrepos/feature/" + feature_dir + "/common_launch_feature.jpg"
    # 中间launching判断
    real_launching_feature_path = path + "/picrepos/feature/" + feature_dir + "/" + device_name + "_launching_feature.jpg"
    real_last_feature_path = path + "/picrepos/feature/" + feature_dir + "/" + device_name + "_homepage_feature.jpg"
    first = first_frame_find(file_count, real_path, real_first_feature_path)  # 取图片这些步骤好繁琐啊，想想有没办法改进下
    launching_index, last = last_and_launching_frame_find_rgb(file_count, first, real_path,
                                                              real_launching_feature_path,
                                                              real_last_feature_path, rgb_folder)
    # frame_value = settings.get_value("ffmpeg")
    frame_value = 50
    total_time = int((last - first + 1) * (1000 / float(frame_value)))
    launching_time = int((launching_index - first + 1) * (1000 / float(frame_value)))
    return dir_index, first, launching_index, last, total_time, launching_time, total_time - launching_time


# 原始数据暂时还没有对异常数据进行刨除
def multi_normal_calculate(device_name, suffix):
    pool = ThreadPool()
    dir_count = count_dirs("./screenrecord/" + device_name + "_" + suffix)
    params = []
    for i in range(0, dir_count):
        params_temp = {"device": device_name, "suffix": suffix, "dir_index": i}
        params.append(params_temp)
    start_time = datetime.datetime.now()
    results = pool.map(multi_normal_calculate_part, params)
    end_time = datetime.datetime.now()
    # 资源回收
    pool.close()
    pool.join()
    print "actual calculate time = {} -------------- {}".format(end_time - start_time, results)
    return results


def multi_huya_calculate(device_name):
    pool = ThreadPool()
    dir_count = count_dirs("./screenrecord/" + device_name + "_first")
    params = []
    for i in range(0, dir_count):
        params_temp = {"device": device_name, "dir_index": i}
        params.append(params_temp)
    start_time = datetime.datetime.now()
    results = pool.map(multi_normal_calculate_part, params)
    end_time = datetime.datetime.now()
    # 资源回收
    pool.close()
    pool.join()
    print "actual calculate time = {} -------------- {}".format(end_time - start_time, results)
    return results


# 每个目录算一次，这种计算只针对特殊启动： 置灰 -> 启动页 -> 登录页/兴趣选择页
def multi_huya_calculate_parts(params):
    device_name = params["device"]  # 设备名称
    name_with_suffix = device_name + "_first"
    dir_index = params["dir_index"]  # 当前算的第几组数据
    # rgb_folder = calculate_homepage_rgb()  # 计算样本库的rgb均值
    conf = Config("apk.ini")
    conf_default = Config("default.ini")
    app_key = conf_default.getconf("default").app
    feature_dir = conf.getconf(app_key).feature  # 特征图的文件夹名字
    file_count = count_file("./screenrecord/" + name_with_suffix + "/" + name_with_suffix + "_" + str(dir_index))
    real_path = "./screenrecord/" + name_with_suffix + "/" + name_with_suffix + "_" + str(dir_index) + "/"
    real_first_feature_path = path + "/picrepos/feature/" + feature_dir + "/" + device_name + "_launch_feature.jpg"
    if not exists(real_first_feature_path):
        MLog.debug("calculate: first, there is no adapted feature pic for current Phone")
        real_first_feature_path = path + "/picrepos/feature/" + feature_dir + "/common_launch_feature.jpg"
    # 中间launching判断
    real_launching_feature_path = path + "/picrepos/feature/" + feature_dir + "/" + device_name + "_launching_feature.jpg"
    real_last_feature_path = path + "/picrepos/feature/" + feature_dir + "/" + device_name + "_homepage_feature.jpg"
    first = first_frame_find(file_count, real_path, real_first_feature_path)  # 取图片这些步骤好繁琐啊，想想有没办法改进下
    launching_index, last = huya_first_find_frame(file_count, first, real_path,
                                                  real_launching_feature_path,
                                                  real_last_feature_path, rgb_folder)  # 虎牙的计算也就只有这句不一样吊
    # frame_value = settings.get_value("ffmpeg")
    frame_value = 50
    total_time = int((last - first + 1) * (1000 / float(frame_value)))
    launching_time = int((launching_index - first + 1) * (1000 / float(frame_value)))
    return dir_index, first, launching_index, last, total_time, launching_time, total_time - launching_time


if __name__ == '__main__':
    multi_normal_calculate("Redmi4A", "notfirst")
