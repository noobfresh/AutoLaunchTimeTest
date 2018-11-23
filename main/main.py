# coding=utf-8
import datetime
import re

from config.configs import Config
from calculate.conclude import calculate

from datachart.charts import *
from datachart.handledata import create_excel
from datachart.sendmail import sendEmailWithDefaultConfig
from log.log import MLog
from screenrecord.screen_record import getDeviceInfo
from screenrecord.screen_record import start_python
import sys

import settings

user_config = False


# 从参数中读取帧率
def init_ffmpeg(ffmpeg):
    settings._init()
    try:
        if (int(ffmpeg) < 0):
            raise Exception('num < 0')

        settings.set_value("ffmpeg", ffmpeg)
    except Exception:
        settings.set_value("ffmpeg", 30)
        print u"未设置帧率，使用默认的帧率值！"

    print u"帧数 = " + str(settings.get_value("ffmpeg"))


if __name__ == '__main__':

    start_time = datetime.datetime.now()

    frame = 0
    first_start = 0
    normal_start = 0
    apk_name = u"yy.apk"

    try:
        if user_config is True:
            print u"使用配置文件参数..."
            conf = Config("default.ini")
            frame = conf.getconf("default").frame
            first_start = conf.getconf("default").first_start
            normal_start = conf.getconf("default").normal_start
            apk_name = conf.getconf("default").apk_name
        else:
            print u"使用命令行输入参数..."
            first_start = sys.argv[1]
            normal_start = sys.argv[2]
            apk_name = sys.argv[3]
            frame = sys.argv[4]
    except Exception:
        MLog.error(u"获取参数错误,使用默认值")
        frame = 30
        first_start = 1
        normal_start = 1
        apk_name = u"yy.apk"

    finally:
        # start_python 需要运行在init_ffmpeg后面，否则拿不到帧数的值
        print "apk = " + str(apk_name) + " ,first_start = " \
              + str(first_start) + " ,normal_start = " + str(normal_start) + " ,frame = " + str(frame)
        init_ffmpeg(int(frame))
        start_python(int(first_start), int(normal_start), str(apk_name))

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
        "start": mean_time2,
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
