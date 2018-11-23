# coding=utf-8
from base_utils import count_dirs, count_file
from first_frame_calculate import first_frame_find
from last_frame_calculate import last_frame_find_rgb
from first_frame_calculate import new_first_frame_find
from last_frame_calculate import new_last_frame_find_rgb
from log.log import MLog
from rgb import calculate_homepage_rgb
from os.path import exists
import settings


def calculate(device_name, name_with_suffix):
    dir_count = count_dirs("./" + name_with_suffix)
    real_num = dir_count  # 真实有效数据个数（存在找不到首帧，或者末尾帧的情况，这种情况下，直接抛弃数据）
    mean_time = 0
    datas = []
    rgb_folder = calculate_homepage_rgb()
    print "dir_count = {}".format(dir_count)
    for i in range(1, dir_count):
        # 取指定目录下的file count
        file_count = count_file(name_with_suffix + "/" + name_with_suffix + "_" + str(i))
        real_path = "./" + name_with_suffix + "/" + name_with_suffix + "_" + str(i) + "/"
        real_first_feature_path = "./feature/" + device_name + "_launch_feature.jpg"
        if not exists(real_first_feature_path):
            print "first, there is no adapted feature pic for current Phone"
            real_first_feature_path = "./feature/common_launch_feature.jpg"
        first = first_frame_find(file_count, real_path, real_first_feature_path)
        # 异常处理
        if first == -1:
            dir_count -= 1
            datas.append(0)
            print "can't not find first frame"
            continue
        # # 中间会生成多余的照片影响
        real_last_feature_path = "./feature/" + device_name + "_homepage_feature.jpg"
        if not exists(real_last_feature_path):
            print "last, there is no adapted feature pic for current Phone"
            real_last_feature_path = "./feature/common_homepage_feature.jpg"
        last = last_frame_find_rgb(file_count, first, real_path, real_last_feature_path, rgb_folder)
        # 异常处理
        if last == -1:
            dir_count -= 1
            datas.append(0)
            print "can't not find first frame"
            continue
        print "帧数 = " + str(settings.get_value("ffmpeg"))
        time = (last - first + 1) * (1000 / int(settings.get_value("ffmpeg")))
        datas.append(time)
        MLog.info("first frame = {}, last frame = {}, time = {}".format(first, last, time))
        mean_time += time
    if dir_count != 0:
        mean_time /= dir_count  # 这个平均时间的逻辑没有考虑到，异常数据的刨除
    print "actually valid count = {}".format(real_num)
    return mean_time, datas


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
        print "first, there is no adapted feature pic for current Phone"
        real_first_feature_path = "./feature/common_launch_feature.jpg"
    # 末帧特征图地址
    real_last_feature_path = "./feature/" + device_name + "_homepage_feature.jpg"
    if not exists(real_last_feature_path):
        print "last, there is no adapted feature pic for current Phone"
        real_last_feature_path = "./feature/common_homepage_feature.jpg"

    first_frame = new_first_frame_find(1, image_count, real_dir_path, real_first_feature_path)
    while first_frame > 0:
        last_frame = new_last_frame_find_rgb(first_frame, image_count, real_dir_path, real_last_feature_path, rgb_folder)
        if last_frame == -1:
            print "i have not found last frame"
            break
        else:
            print "帧数 = " + str(settings.get_value("ffmpeg"))
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