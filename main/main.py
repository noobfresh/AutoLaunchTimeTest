# coding=utf-8
import datetime
import json
import os
import re


from datachart.charts import create_line
from datachart.handledata import create_sheet
from datachart.sendmail import sendEmailWithDefaultConfig
from screen_record import getDeviceInfo
from screen_record import start_python
from calculate.conclude import calculate


def utf8(file_name):
    return file_name.decode('utf-8')


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    start_python()
    end_video_2_frame_time = datetime.datetime.now()
    print u"录屏及切帧时间 time = {}".format(end_video_2_frame_time - start_time)
    # ---------------------------- Calculate part ------------------------------#
    #
    # 生成好照片
    device_name = getDeviceInfo()
    device_name = re.sub('\s', '', device_name)
    mean_time1, datas1 = calculate(device_name, device_name + "_first")
    mean_time2, datas2 = calculate(device_name, device_name + "_notfirst")
    # mean_time2, datas2 = "0", [0]
    end_calculate_time = datetime.datetime.now()
    print u"计算时间 time ={}".format(end_calculate_time - end_video_2_frame_time)

    # ---------------------------- UI part ------------------------------#

    json_data = [{
        "phone": device_name,
        "app": "7.11.1",
        "first_start": mean_time1,
        "start": mean_time1,
        "home": ""
    }]

    if len(datas1) > len(datas2):
        for i in range(len(datas1) - len(datas2)):
            datas2.append(0)
    elif len(datas2) > len(datas1):
        for i in range(len(datas2) - len(datas1)):
            datas1.append(0)

    json_datas = [
        {
            "app": u"7.11 首次启动",
            "datas": datas1
        },
        {
            "app": u"7.11 非首次启动",
            "datas": datas2
        }
    ]

    print json.dumps(json_data)

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
    file_name = "data_result"
    json_file_path = "data.json"
    create_sheet(sheet_name, utf8(file_name), json_file_path)

    json_file_name = "datas.json"
    phone_type = device_name
    title = phone_type + u"首次启动耗时"
    result_name = "chart"
    create_line(json_file_name, title, result_name)

    sendEmailWithDefaultConfig()

    print json.dumps(json_data)
    end_time = datetime.datetime.now()
    print "all time = {}, video_frame time = {}, calculate time = {}, datacharts time = {}".format(
        end_time - start_time,
        end_video_2_frame_time - start_time,
        end_calculate_time - end_video_2_frame_time,
        end_time - end_calculate_time)
    # 强行结束
    os._exit(0)
