# coding=utf-8
import json
import os
import re

from calculate.base_utils import count_dirs
from calculate.base_utils import count_file
from calculate.clip import clip
from calculate.first_frame_calculate import first_frame_find
from calculate.last_frame_calculate import last_frame_find_rgb
from screen_record import getDeviceInfo
from datachart.charts import create_line
from datachart.handledata import create_sheet
from datachart.sendmail import sendEmailWithDefaultConfig


def utf8(file_name):
    return file_name.decode('utf-8')


if __name__ == '__main__':
    # start_python()
    #

    # 生成好照片
    # device_name = getDeviceInfo()
    # device_name = re.sub('\s', '', device_name)
    # # print device_name
    # dir_count = count_dirs("./" + device_name)
    # obj = {"app": "7.12", "phone": device_name}
    # mean_time = 0
    # for i in range(0, dir_count):
    #     # 取指定目录下的file count
    #     file_count = count_file(device_name + "/" + device_name + "_" + str(i))
    #     real_path = "./" + device_name + "/" + device_name + "_" + str(i) + "/"
    #     # 优化点，没有必要全裁一遍其实
    #     clip(real_path, file_count)
    #     real_first_feature_path = "./feature/" + device_name + "_launch_feature.jpg"
    #     first = first_frame_find(file_count, real_path, real_first_feature_path)
    #     # # 中间会生成多余的照片影响
    #     real_last_feature_path = "./feature/" + device_name + "_homepage_feature.jpg"
    #     last = last_frame_find_rgb(file_count, first, real_path, real_last_feature_path)
    #     time = (last - first + 1) * (1000 / 60)
    #     print "first frame = {}, last frame = {}, time = {}".format(first, last, time)
    #     mean_time += time
    # mean_time /= dir_count
    # obj["first_start"] = str(mean_time)
    # obj["start"] = ""
    # json_data = [obj]

    json_data = [{
        "phone": "OPPO R9s",
        "app": "7.11.1",
        "first_start": "7.17",
        "start": "5.65",
        "home": "0.15"
    }]

    json_datas = [
        {
            "app": "7.11",
            "datas": [
                8266.67,
                6233.33,
                7300,
                7266.67,
                6766.67
            ]
        },
        # {
        #     "app": "7.12",
        #     "datas": [
        #         5600,
        #         5366.67,
        #         5466.67,
        #         5133.33,
        #         4966.67
        #     ]
        # },
        # {
        #     "app": "虎牙",
        #     "datas": [
        #         4600,
        #         5366.67,
        #         4466.67,
        #         6133.33,
        #         4966.67
        #     ]
        # },
        # {
        #     "app": "陌陌",
        #     "datas": [
        #         4700,
        #         4366.67,
        #         4466.67,
        #         4133.33,
        #         5266.67
        #     ]
        # }
    ]

    print "#########原始数据##########"
    print "excel表格数据:"
    print json.dumps(json_data)

    print "柱状图数据:"
    print json.dumps(json_datas)

    ################ 写入 #####################
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
    create_line(json_file_name, title,result_name)

    sendEmailWithDefaultConfig()

    print json.dumps(json_data)
