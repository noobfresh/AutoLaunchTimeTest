# coding=utf-8
import datetime

from calculate.base_utils import count_dirs, count_file
from calculate.clip import clip
from calculate.first_frame_calculate import first_frame_find
from calculate.last_frame_calculate import last_frame_find_rgb
from screen_record import start_python
from screen_record import getDeviceInfo
from datachart.charts import create_line
from datachart.handledata import create_sheet
from datachart.sendmail import sendEmailWithDefaultConfig
import re
import json
import time


def utf8(file_name):
    return file_name.decode('utf-8')


if __name__ == '__main__':
    start = datetime.datetime.now()
    start_python()
    #
    # 生成好照片
    device_name = getDeviceInfo()
    device_name = re.sub('\s', '', device_name)
    # time.sleep(5)
    dir_count = count_dirs("./" + device_name)
    obj = {"app": "7.12", "phone": device_name}
    real_num = dir_count  # 真实有效数据个数（存在找不到首帧，或者末尾帧的情况，这种情况下，直接抛弃数据）
    mean_time = 0
    datas = []
    print "dir_count = {}".format(dir_count)
    for i in range(0, dir_count):
        # 取指定目录下的file count
        file_count = count_file(device_name + "/" + device_name + "_" + str(i))
        real_path = "./" + device_name + "/" + device_name + "_" + str(i) + "/"
        # 优化点，没有必要全裁一遍其实
        clip(real_path, file_count)
        real_first_feature_path = "./feature/" + device_name + "_launch_feature.jpg"
        first = first_frame_find(file_count, real_path, real_first_feature_path)
        # 异常处理
        if first == -1:
            dir_count -= 1
            datas.append(0)
            print "can't not find first frame"
            continue
        # # 中间会生成多余的照片影响
        real_last_feature_path = "./feature/" + device_name + "_homepage_feature.jpg"
        last = last_frame_find_rgb(file_count, first, real_path, real_last_feature_path)
        # 异常处理
        if last == -1:
            dir_count -= 1
            datas.append(0)
            print "can't not find first frame"
            continue
        time = (last - first + 1) * (1000 / 60)
        datas.append(time)
        print "first frame = {}, last frame = {}, time = {}".format(first, last, time)
        mean_time += time
    if dir_count != 0:
        mean_time /= dir_count  # 这个平均时间的逻辑没有考虑到，异常数据的刨除
    print "actually valid count = {}".format(real_num)
    obj["first_start"] = str(mean_time)
    obj["start"] = ""
    json_data = [obj]
    print json.dumps(json_data)
    json_data = [{
        "phone": "OPPO R9s",
        "app": "7.11.1",
        "first_start": mean_time,
        "start": "",
        "home": ""
    }]

    json_datas = [
        {
            "app": "7.11",
            "datas": datas
        }
    ]

    print "#########原始数据##########"
    print "excel表格数据:"
    print json.dumps(json_data)

    print "柱状图数据:"
    print json.dumps(json_datas)

    # --------------------    写入    -----------------------#
    fileObject = open('data.json', 'w')
    fileObject.write(json.dumps(json_data))
    fileObject.close()

    fileObject = open('datas.json', 'w')
    fileObject.write(json.dumps(json_datas))
    fileObject.close()

    #######################################
    sheet_name = "time_cost"
    file_name = "测试结果"
    json_file_path = "data.json"
    create_sheet(sheet_name, utf8(file_name), json_file_path)

    json_file_name = "datas.json"
    phone_type = "oppo r9s"
    title = phone_type + "首次启动耗时"
    result_name = "柱状图"
    create_line(json_file_name, title, result_name)

    sendEmailWithDefaultConfig()

    print json.dumps(json_data)
    end = start = datetime.datetime.now()
    print "all time = {}".format(end - start)
