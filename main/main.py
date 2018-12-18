# coding=utf-8
import datetime

from calculate.conclude import multi_huya_calculate, multi_normal_calculate
from config.configs import Config
from config.sys_config import get_start_params, get_device_params, getApkName
from datachart.charts import *
from datachart.data_center import write_data_to_file
from datachart.data_to_format import format_data, create_sheet
from datachart.sendmail import sendEmailWithDefaultConfig
from log.log import MLog
from screenrecord.screen_record_main import start_python

if __name__ == '__main__':

    MLog.debug(u"程序启动...")
    start_time = datetime.datetime.now()

    firstLaunchTimes, notFirstLaunchTimes, apkName = get_start_params()
    start_python(firstLaunchTimes, notFirstLaunchTimes, apkName)

    end_video_2_frame_time = datetime.datetime.now()

    MLog.info(u"录屏及切帧时间 time = {}".format(end_video_2_frame_time - start_time))
    # ---------------------------- Calculate part ------------------------------#
    # 主动切换一下cmd的当前路径
    path = os.path.dirname(__file__) + "\\"
    os.chdir(path)
    device_name = get_device_params()
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

    json_datas1, json_datas2, json_detail, dict1, json_detail2, dict2 = format_data()
    end_calculate_time = datetime.datetime.now()
    MLog.info(u"计算时间 time ={}".format(end_calculate_time - end_video_2_frame_time))

    write_data_to_file(u"首次启动总耗时", device_name, getApkName().split(".apk")[0], json_datas1)
    write_data_to_file(u"非首次启动总耗时", device_name, getApkName().split(".apk")[0], json_datas2)

    create_sheet(json_detail, dict1, json_detail2, dict2)
    end_handle_data_time = datetime.datetime.now()
    MLog.info(u"生成图表和表格时间 time ={}".format(end_handle_data_time - end_calculate_time))

    # ---------------------------- UI part ------------------------------#

    sendEmailWithDefaultConfig()

    end_time = datetime.datetime.now()
    MLog.info("all time = {}, video_frame time = {}, calculate time = {}, datacharts time = {}".format(
        end_time - start_time,
        end_video_2_frame_time - start_time,
        end_calculate_time - end_video_2_frame_time,
        end_time - end_calculate_time))
    # 强行结束
    os._exit(0)
