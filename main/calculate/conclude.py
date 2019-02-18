# coding=utf-8
import datetime
import traceback
from multiprocessing.dummy import Pool as ThreadPool
from os.path import exists
from multiprocessing import cpu_count
import settings
from base_utils import count_dirs, count_file
from config.configs import Config
from first_frame_calculate import first_frame_find, enter_ent_first_frame_find
from last_frame_calculate import last_and_launching_frame_find_rgb, huya_first_find_frame, enter_ent_last_frame_find, \
    enter_ent_last_frame_find_fade_in, enter_ent_last_frame_find_fade_in_test
from log.log import MLog
from rgb import calculate_homepage_rgb
from screenrecord.screen_record_main import getDevices

conf = Config("default.ini")
path = conf.getconf("default").feature_path
# rgb_folder = calculate_homepage_rgb()  # 计算样本库的rgb均值
rgb_folder = [183, 183, 183]
cpu_num = cpu_count()


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
    # file_count = 749
    real_first_feature_path = path + "/picrepos/feature/" + feature_dir + "/" + device_name + "_launch_feature.jpg"
    if not exists(real_first_feature_path):
        MLog.debug("calculate: first, there is no adapted feature pic for current Phone")
        real_first_feature_path = path + "/picrepos/feature/" + feature_dir + "/common_launch_feature.jpg"
    # 中间launching判断
    real_launching_feature_path = path + "/picrepos/feature/" + feature_dir + "/" + device_name + "_launching_feature.jpg"
    real_last_feature_path = path + "/picrepos/feature/" + feature_dir + "/" + device_name + "_homepage_feature.jpg"
    #########################
    first = first_frame_find(file_count, real_path, real_first_feature_path)  # 取图片这些步骤好繁琐啊，想想有没办法改进下
    if first == -1:
        return dir_index, 0, 0, 0, 0, 0, 0
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
    # 感觉这个有点乱来
    device_len = len(getDevices())
    num = cpu_num - 1 - device_len
    if num <= 0:
        num = 1
    pool = ThreadPool(num)
    dir_count = count_dirs("./screenrecord/" + device_name + "_" + suffix)
    params = []
    results = []
    start_time = datetime.datetime.now()
    for i in range(0, dir_count):
        params_temp = {"device": device_name, "suffix": suffix, "dir_index": i}
        params.append(params_temp)
        # results.append(multi_normal_calculate_part(params_temp))
    results = pool.map(multi_normal_calculate_part, params)
    end_time = datetime.datetime.now()
    # 资源回收
    pool.close()
    pool.join()
    print "actual calculate time = {} -------------- {}".format(end_time - start_time, results)
    return results


def multi_huya_calculate(device_name):
    device_len = len(getDevices())
    num = cpu_num - 1 - device_len
    if num <= 0:
        num = 1
    pool = ThreadPool(num)
    dir_count = count_dirs("./screenrecord/" + device_name + "_first")
    params = []
    results = []
    start_time = datetime.datetime.now()
    for i in range(0, dir_count):
        params_temp = {"device": device_name, "dir_index": i}
        params.append(params_temp)
        # results.append(multi_huya_calculate_parts(params))
    # start_time = datetime.datetime.now()
    results = pool.map(multi_normal_calculate_part, params)
    end_time = datetime.datetime.now()
    # 资源回收
    # pool.close()
    # pool.join()
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


def enter_ent_calcucate(device_name):
    top_x = settings.get_value("ent_top_pos_x")  # 这个是进入直播间计算速度计算
    top_y = settings.get_value("ent_top_pos_y")
    print "top_x = {}, topy_y = {}".format(top_x, top_y)
    dir_count = count_dirs("./screenrecord/" + device_name + "_enterliveroom/")
    print "dir_count = {}".format(dir_count)
    for i in range(dir_count):
        enter_ent_calculate_part("./screenrecord/" + device_name + "_enterliveroom/" + device_name + "_enterliveroom_" +
                                 str(i) + "/", top_x, top_y)


def enter_ent_calculate_new(device_name):
    top_x = settings.get_value("ent_top_pos_x")  # 这个是进入直播间计算速度计算
    top_y = settings.get_value("ent_top_pos_y")
    print "top_x = {}, topy_y = {}".format(top_x, top_y)
    dir_count = count_dirs("./screenrecord/" + device_name + "_enterliveroom/")
    print "dir_count = {}".format(dir_count)
    device_len = len(getDevices())
    num = cpu_num - 1 - device_len
    if num <= 0:
        num = 1
    pool = ThreadPool(num)
    params = []
    results = []
    start_time = datetime.datetime.now()
    for i in range(0, dir_count):
        path = "./screenrecord/" + device_name + "_enterliveroom/" + device_name + "_enterliveroom_" + str(i) + "/"
        params_temp = {"path": path, "top_x": top_x, "top_y": top_y}
        params.append(params_temp)
    results = pool.map(enter_ent_calculate_part, params)
    end_time = datetime.datetime.now()
    pool.close()
    pool.join()
    print "actual calculate time = {} -------------- {}".format(end_time - start_time, results)
    return results


def enter_ent_calculate_part(params):
    path = params["path"]
    top_x = params["top_x"]
    top_y = params["top_y"]
    return enter_ent_calculate_part_inner(path, top_x, top_y)


def enter_ent_calculate_part_inner(path, x, y):
    file_count = count_file(path)
    first_index = enter_ent_first_frame_find(file_count, path, x, y)
    print "first_index = {}".format(first_index)
    # feature_path = settings.get_value("feature_path")
    enter_live_room_index, last_index = enter_ent_last_frame_find_fade_in_test(first_index, file_count, path)
    print "first_index = {}, the enter_live_room_index = {}, last index = {}".format(first_index, enter_live_room_index,
                                                                                     last_index)
    return first_index, enter_live_room_index, last_index


def start_calculate(device_name):
    conf_default = Config("default.ini")
    app_key = conf_default.getconf("default").app
    first_launch_result = []
    normal_launch_result = []
    if app_key == "huya" or app_key == "momo":
        first_launch_result = multi_huya_calculate(device_name)
    else:
        first_launch_result = multi_normal_calculate(device_name, "first")
    # 以后想适配虎牙陌陌的话，必须uiautomator那边要手动处理下登录/跳过
    normal_launch_result = multi_normal_calculate(device_name, "notfirst")
    # TODO 如果进直播间测试次数设置为0，会崩溃，杨帆后续改
    try:
        enter_ent_result = enter_ent_calculate_new(device_name)
    except Exception, e:
        MLog.error(u"测试进直播间计算的时候出现崩溃了 + error = ")
        MLog.error(traceback.format_exc(e))
        enter_ent_result = []

    return first_launch_result, normal_launch_result, enter_ent_result


if __name__ == '__main__':
    start_calculate("MI8")
    print 1
