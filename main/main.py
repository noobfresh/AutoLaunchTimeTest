# coding=utf-8
import collections
import datetime
import re
import sys

import settings
from calculate.conclude import calculate, new_new_calculate, huya_first_calculate
from config.configs import Config
from datachart.charts import *
from datachart.handledata import create_detail_sheet_by_json
from datachart.sendmail import sendEmailWithDefaultConfig
from log.log import MLog
from screenrecord.device_info import getDeviceInfo
from screenrecord.screen_record_main import start_python

user_config = True


# 从参数中读取帧率
def init_ffmpeg(ffmpeg):
    os.system('adb shell pm clear com.github.uiautomator')
    settings._init()
    try:
        if (int(ffmpeg) < 0):
            raise Exception('num < 0')

        settings.set_value("ffmpeg", ffmpeg)
    except Exception:
        settings.set_value("ffmpeg", 30)
        print u"未设置帧率，使用默认的帧率值！"

    print u"帧数 = " + str(settings.get_value("ffmpeg"))


# 去掉最低最高取平均
def avg_list(list):
    nsum = 0
    count = 0
    for i in range(len(list)):
        if list[i] != 0:
            nsum += list[i]
            count += 1
    if count == 0:
        return 0
    if count < 4:
        return nsum / count
    highest = max(list)
    lowest = min(list)
    nsum -= highest
    nsum -= lowest
    count -= 2
    return nsum / count


if __name__ == '__main__':

    MLog.debug(u"程序启动...")
    start_time = datetime.datetime.now()

    frame = 30
    first_start = 1
    normal_start = 1
    apk_name = u"70003.apk"

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
        MLog.info("apk = " + str(apk_name) + " ,first_start = " \
              + str(first_start) + " ,normal_start = " + str(normal_start) + " ,frame = " + str(frame))
        init_ffmpeg(int(frame))
        start_python(int(first_start), int(normal_start), str(apk_name))

    # init_ffmpeg(int(frame))
    end_video_2_frame_time = datetime.datetime.now()
    MLog.info(u"录屏及切帧时间 time = {}".format(end_video_2_frame_time - start_time))
    # ---------------------------- Calculate part ------------------------------#
    #
    # 生成好照片
    path = os.path.dirname(__file__) + "\\"
    os.chdir(path)
    conf = Config("default.ini")
    event = conf.getconf("serial").serial_number
    serial = event.split(',')
    device_name = getDeviceInfo(serial[0])
    device_name = re.sub('\s', '', device_name)
    # mean_time1, datas1 = new_calculate(device_name, device_name + "_first", True, first_start)
    # mean_time2, datas2 = new_calculate(device_name, device_name + "_notfirst", False, normal_start)
    conf_default = Config("default.ini")
    app_key = conf_default.getconf("default").app
    if app_key == "huya":
        mean_time1, datas1, launchingdatas1 = huya_first_calculate(device_name, device_name + "_first")
    else:
        mean_time1, datas1, launchingdatas1 = new_new_calculate(device_name, device_name + "_first")
    mean_time2, datas2, launchingdatas2 = new_new_calculate(device_name, device_name + "_notfirst")
    end_calculate_time = datetime.datetime.now()
    MLog.info(u"计算时间 time ={}".format(end_calculate_time - end_video_2_frame_time))

    # ---------------------------- UI part ------------------------------#
    if len(datas1) > len(datas2):
        for i in range(len(datas1) - len(datas2)):
            datas2.append(0)
    elif len(datas2) > len(datas1):
        for i in range(len(datas2) - len(datas1)):
            datas1.append(0)

    if len(launchingdatas1) > len(launchingdatas2):
        for i in range(len(launchingdatas1) - len(launchingdatas2)):
            launchingdatas2.append(0)
    elif len(launchingdatas2) > len(launchingdatas1):
        for i in range(len(launchingdatas2) - len(launchingdatas1)):
            launchingdatas1.append(0)

    if len(datas1) > len(launchingdatas1):
        for i in range(len(datas1) - len(launchingdatas1)):
            launchingdatas1.append(0)
    elif len(launchingdatas1) > len(datas1):
        for i in range(len(launchingdatas1) - len(datas1)):
            datas1.append(0)

    if len(datas2) > len(launchingdatas2):
        for i in range(len(datas2) - len(launchingdatas2)):
            launchingdatas2.append(0)
    elif len(launchingdatas2) > len(datas2):
        for i in range(len(launchingdatas2) - len(datas2)):
            datas2.append(0)

    json_datas = [
        {
            "app": apk_name + "首次启动总耗时",
            "datas": datas1
        },
        {
            "app": apk_name + "首次启动耗时",
            "datas": launchingdatas1
        }
    ]

    json_datas2 = [
        {
            "app": apk_name + "非首次启动总耗时",
            "datas": datas2
        },
        {
            "app": apk_name + "非首次启动耗时",
            "datas": launchingdatas2
        }
    ]

    MLog.info(json.dumps(datas1))
    MLog.info(json.dumps(launchingdatas1))
    MLog.info(json.dumps(datas2))
    MLog.info(json.dumps(launchingdatas2))

    # 生成折线图
    result_name = "chart"
    chart1 = ChartItem(device_name + " 首次启动耗时", json_datas)
    chart2 = ChartItem(device_name + " 非首次启动耗时", json_datas2)
    chart_items = [chart1, chart2]

    create_charts(result_name, chart_items)

    sheet_name = "detail_time_cost"
    file_name = "data_detail"
    json_file_path = "data.json"

    json_detail = []
    for i in range(1, len(datas1) + 1):
        dict_temp = {"a": str(i),
                     "b": str(datas1[i-1]),
                     "c": str(launchingdatas1[i-1]),
                     "d": str(datas1[i-1] - launchingdatas1[i-1]),
                     "e": str(datas2[i-1]),
                     "f": str(launchingdatas2[i-1]),
                     "g": str(datas2[i-1] - launchingdatas2[i-1])}
        json_detail.append(dict_temp)
    MLog.info(json.dumps(json_detail))
    dict1 = collections.OrderedDict()
    dict1["a"] = u"次数"
    dict1["b"] = u"首次启动总耗时"
    dict1["c"] = u"首次启动耗时"
    dict1["d"] = u"首次启动首页加载耗时"
    dict1["e"] = u"非首次启动总耗时"
    dict1["f"] = u"非首次启动耗时"
    dict1["g"] = u"非首次启动首页加载耗时"
    MLog.info(json.dumps(json_detail))
    MLog.info(json.dumps(dict1))
    create_detail_sheet_by_json(sheet_name, file_name, device_name + " " + apk_name + u" 耗时统计", json_detail, dict1)
    print "--------------------------------------------------------"
    json_detail2 = []
    dict_avg = {
                  "a": avg_list(datas1),
                  "b": avg_list(launchingdatas1),
                  "c": avg_list(datas1) - avg_list(launchingdatas1),
                  "d": avg_list(datas2),
                  "e": avg_list(launchingdatas2),
                  "f": avg_list(datas2) - avg_list(launchingdatas2)}
    json_detail2.append(dict_avg)
    dict2 = collections.OrderedDict()
    dict2["a"] = u"平均首次启动总耗时"
    dict2["b"] = u"平均首次启动耗时"
    dict2["c"] = u"平均首次启动首页加载耗时"
    dict2["d"] = u"平均非首次启动总耗时"
    dict2["e"] = u"平均非首次启动耗时"
    dict2["f"] = u"平均非首次启动首页加载耗时"
    MLog.info(json.dumps(json_detail2))
    MLog.info(json.dumps(dict2))
    print "--------------------------------------------------------"
    create_detail_sheet_by_json(sheet_name, "data_result", device_name + " " + apk_name + u" 平均耗时统计",
                                json_detail2, dict2)

    sendEmailWithDefaultConfig()

    end_time = datetime.datetime.now()
    MLog.info("all time = {}, video_frame time = {}, calculate time = {}, datacharts time = {}".format(
        end_time - start_time,
        end_video_2_frame_time - start_time,
        end_calculate_time - end_video_2_frame_time,
        end_time - end_calculate_time))
    # 强行结束
    os._exit(0)
