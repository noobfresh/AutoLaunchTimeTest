# coding=utf-8
from base_utils import count_dirs, count_file
from calculate.launching_frame_calculate import find_lanching_end_frame
from config.configs import Config
from first_frame_calculate import first_frame_find
from last_frame_calculate import last_frame_find_rgb
from first_frame_calculate import new_first_frame_find
from last_frame_calculate import new_last_frame_find_rgb
from log.log import MLog
from rgb import calculate_homepage_rgb
from os.path import exists
import settings


def calculate(device_name, name_with_suffix):
    dir_count = count_dirs("./screenrecord/" + name_with_suffix)
    real_num = dir_count  # 真实有效数据个数（存在找不到首帧，或者末尾帧的情况，这种情况下，直接抛弃数据）
    mean_time = 0
    datas = []
    launching_datas = []
    rgb_folder = calculate_homepage_rgb()
    MLog.debug("calculate: dir_count = {}".format(dir_count))
    conf = Config("apk.ini")
    feature_dir = conf.getconf("yy").feature
    for i in range(0, dir_count):
        # 取指定目录下的file count
        file_count = count_file("screenrecord/" + name_with_suffix + "/" + name_with_suffix + "_" + str(i))
        real_path = "./screenrecord/" + name_with_suffix + "/" + name_with_suffix + "_" + str(i) + "/"
        real_first_feature_path = "./picrepos/feature/" + feature_dir + "/" + device_name + "_launch_feature.jpg"
        if not exists(real_first_feature_path):
            MLog.debug("calculate: first, there is no adapted feature pic for current Phone")
            real_first_feature_path = "./picrepos/feature/" + feature_dir + "/common_launch_feature.jpg"
        first = first_frame_find(file_count, real_path, real_first_feature_path)
        # 异常处理
        if first == -1:
            dir_count -= 1
            datas.append(0)
            launching_datas.append(0)
            MLog.debug("calculate: can't not find first frame")
            continue

        # 中间launching判断
        real_launching_feature_path = "./picrepos/feature/" + feature_dir + "/" + device_name + "_launching_feature.jpg"
        # 做了个特殊处理，获取到首帧过后，跳过了半秒的帧数，为了直接就开始计算启动过程中帧
        launching_index = find_lanching_end_frame(first + int(settings.get_value("ffmpeg")),
                                                  file_count, real_launching_feature_path, real_path)
        if launching_index == -1:
            dir_count -= 1
            datas.append(0)
            launching_datas.append(0)
            MLog.debug("calculate: can't not find launching frame")
            continue
        launching_time = (launching_index - first + 1) * (1000 / int(settings.get_value("ffmpeg")))
        launching_datas.append(launching_time)
        # # 中间会生成多余的照片影响
        real_last_feature_path = "./picrepos/feature/" + feature_dir + "/" + device_name + "_homepage_feature.jpg"
        if not exists(real_last_feature_path):
            MLog.debug("calculate: last, there is no adapted feature pic for current Phone")
            real_last_feature_path = "./picrepos/feature/" + feature_dir + "/common_homepage_feature.jpg"
        last = last_frame_find_rgb(file_count, launching_index, real_path, real_last_feature_path, rgb_folder)
        # 异常处理
        if last == -1:
            dir_count -= 1
            datas.append(0)
            launching_datas.append(0)
            MLog.debug("calculate: can't not find first frame")
            continue
        MLog.debug(u"帧数 = " + str(settings.get_value("ffmpeg")))
        time = (last - first + 1) * (1000 / int(settings.get_value("ffmpeg")))
        datas.append(time)
        MLog.info("first frame = {}, last frame = {}， launching end frame = {}, time = {}".format(
            first, last, launching_index, time))
        mean_time += time
    if dir_count != 0:
        mean_time /= dir_count  # 这个平均时间的逻辑没有考虑到，异常数据的刨除
    MLog.debug("calculate: actually valid count = {}".format(real_num))
    return mean_time, datas, launching_datas


# 现在由于只录一整个视频，所以就不去循环
def new_calculate(device_name, name_with_suffix, is_first, input_num):
    suffix = ""
    if is_first:
        suffix = "first"
    else:
        suffix = "notfirst"
    real_dir_path = "./screenrecord/" + name_with_suffix + "/" + name_with_suffix + "_" + suffix + "/"
    count_num = 0
    mean_time = 0
    datas = []
    rgb_folder = calculate_homepage_rgb()
    image_count = count_file("screenrecord/" + name_with_suffix + "/" + name_with_suffix + "_" + suffix)
    # 首帧特征图地址
    real_first_feature_path = "./feature/" + device_name + "_launch_feature.jpg"
    if not exists(real_first_feature_path):
        MLog.debug("new_calculate: first, there is no adapted feature pic for current Phone")
        real_first_feature_path = "./feature/common_launch_feature.jpg"
    # 末帧特征图地址
    real_last_feature_path = "./feature/" + device_name + "_homepage_feature.jpg"
    if not exists(real_last_feature_path):
        MLog.debug("new_calculate: last, there is no adapted feature pic for current Phone")
        real_last_feature_path = "./feature/common_homepage_feature.jpg"

    first_frame = new_first_frame_find(1, image_count, real_dir_path, real_first_feature_path)
    while first_frame > 0:
        last_frame = new_last_frame_find_rgb(first_frame, image_count, real_dir_path, real_last_feature_path, rgb_folder)
        if last_frame == -1:
            MLog.debug("new_calculate: i have not found last frame")
            break
        else:
            MLog.debug(u"new_calculate: 帧数 = " + str(settings.get_value("ffmpeg")))
            time = (last_frame - first_frame + 1) * (1000 / int(settings.get_value("ffmpeg")))
            datas.append(time)
            mean_time += time
            count_num += 1
            MLog.info("first frame = {}, last frame = {}, time = {}".format(first_frame, last_frame, time))

            if count_num == input_num:
                break

            first_frame = new_first_frame_find(last_frame, image_count, real_dir_path, real_first_feature_path)

    if count_num != 0:
        mean_time /= count_num
    return mean_time, datas