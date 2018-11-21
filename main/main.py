# coding=utf-8
import datetime
import re

from calculate.conclude import calculate
from datachart.charts import *
from datachart.handledata import create_excel
from datachart.sendmail import sendEmailWithDefaultConfig
from screen_record import getDeviceInfo
from screen_record import start_python
import sys

if __name__ == '__main__':
    start_time = datetime.datetime.now()
    start_python(sys.argv[1], sys.argv[2], sys.argv[3])
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

    # 生成excel表格
    sheet_name = "time_cost"
    file_name = "data_result"
    create_excel(sheet_name, file_name, json_data)

    # 生成折线图
    result_name = "chart"
    chart1 = ChartItem(device_name + "首次启动耗时", json_datas)
    chart2 = ChartItem(device_name + "非首次启动耗时", json_datas)
    chart_items = [chart1, chart2]

    create_charts(result_name, chart_items)

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
