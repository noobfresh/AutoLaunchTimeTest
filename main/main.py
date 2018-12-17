# coding=utf-8
import collections
import datetime
import json
import re

from calculate.conclude import multi_huya_calculate, multi_normal_calculate
from config.configs import Config
from datachart.charts import *
from datachart.data_center import write_data_to_file
from datachart.handledata import create_detail_sheet_by_json
from datachart.sendmail import sendEmailWithDefaultConfig
from log.log import MLog
from screenrecord.device_info import getDeviceInfo
from screenrecord.screen_record_main import start_python

user_config = True


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

        start_python(int(first_start), int(normal_start), str(apk_name))

    end_video_2_frame_time = datetime.datetime.now()
    MLog.info(u"录屏及切帧时间 time = {}".format(end_video_2_frame_time - start_time))
    # ---------------------------- Calculate part ------------------------------#
    #
    # 主动切换一下cmd的当前路径
    path = os.path.dirname(__file__) + "\\"
    os.chdir(path)
    conf = Config("default.ini")
    event = conf.getconf("serial").serial_number
    serial = event.split(',')
    device_name = getDeviceInfo(serial[0])  # device name 看看韦总到时候怎么处理，把这一个干掉，我这边的操作其实很多余
    device_name = re.sub('\s', '', device_name)
    conf_default = Config("default.ini")
    app_key = conf_default.getconf("default").app
    if app_key == "huya" or app_key == "momo":
        first_launch_result = multi_huya_calculate(device_name)
    else:
        first_launch_result = multi_normal_calculate(device_name, "first")
    # 以后想适配虎牙陌陌的话，必须uiautomator那边要手动处理下登录/跳过
    normal_launch_result = multi_normal_calculate(device_name, "notfirst")
    # 算平均值啥的
    total_datas1 = []
    launching_datas1 = []
    homepage_datas1 = []
    for i in range(0, len(first_launch_result)):
        total_datas1.append(first_launch_result[i][4])
        launching_datas1.append(first_launch_result[i][5])
        homepage_datas1.append(first_launch_result[i][6])
    total_datas2 = []
    launching_datas2 = []
    homepage_datas2 = []
    for i in range(0, len(normal_launch_result)):
        total_datas2.append(normal_launch_result[i][4])
        launching_datas2.append(normal_launch_result[i][5])
        homepage_datas2.append(normal_launch_result[i][6])
    end_calculate_time = datetime.datetime.now()
    MLog.info(u"计算时间 time ={}".format(end_calculate_time - end_video_2_frame_time))

    # ---------------------------- UI part ------------------------------#
    apk_name = apk_name.split(".apk")[0]
    print apk_name + "   *****************************"
    json_datas1 = {
        "app": apk_name,
        "datas": total_datas1
    }

    json_datas2 = {
        "app": apk_name,
        "datas": total_datas2
    }

    MLog.info(json.dumps(json_datas1))
    MLog.info(json.dumps(json_datas2))
    write_data_to_file(u"首次启动总耗时", device_name, apk_name, json_datas1)
    write_data_to_file(u"非首次启动总耗时", device_name, apk_name, json_datas2)

    sheet_name = "detail_time_cost"
    file_name = "data_detail"
    json_file_path = "data.json"

    json_detail = []
    for i in range(1, len(total_datas1) + 1):
        dict_temp = {"a": str(i),
                     "b": str(total_datas1[i - 1]),
                     "c": str(launching_datas1[i - 1]),
                     "d": str(homepage_datas1[i - 1]),
                     "e": str(total_datas2[i - 1]),
                     "f": str(launching_datas2[i - 1]),
                     "g": str(homepage_datas2[i - 1])}
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
        "a": avg_list(total_datas1),
        "b": avg_list(launching_datas1),
        "c": avg_list(homepage_datas1),
        "d": avg_list(total_datas2),
        "e": avg_list(launching_datas2),
        "f": avg_list(homepage_datas2)}
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
