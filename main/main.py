# coding=utf-8
import datetime
from multiprocessing import Pool
import time
from calculate.conclude import start_calculate
from config.sys_config import get_start_params, getApkName
from datachart.charts import *
from datachart.data_center import write_data_to_file
from datachart.data_to_format import format_data, create_sheet, create_lines
from datachart.sendmail import sendEmailWithDefaultConfig
from log.log import MLog
from screenrecord.device_info import getDeviceInfo
from screenrecord.screen_record_main import start_python, getDevices


def test_main(serial_num):
    firstLaunchTimes, notFirstLaunchTimes, enterLiveTimes,apkName = get_start_params()
    MLog.info("current Device = {}".format(serial_num))
    start_time = datetime.datetime.now()
    start_python(firstLaunchTimes, notFirstLaunchTimes,enterLiveTimes, apkName, serial_num)
    end_video_2_frame_time = datetime.datetime.now()
    MLog.info(u"录屏及切帧时间 time = {}".format(end_video_2_frame_time - start_time))

    path = os.path.dirname(__file__) + "\\"
    os.chdir(path)
    device_name = getDeviceInfo(serial_num)
    first_launch_result, normal_launch_result = start_calculate(device_name)
    json_datas1, json_datas2, json_detail, dict1, json_detail2, dict2, launching_datas1, launching_datas2 = format_data(
        first_launch_result,
        normal_launch_result,
        apkName)
    end_calculate_time = datetime.datetime.now()
    MLog.info(u"计算时间 time ={}".format(end_calculate_time - end_video_2_frame_time))

    # ---------------------------- UI part ------------------------------#

    # 写 JSON 数据
    write_data_to_file(u"首次启动总耗时", device_name, getApkName().split(".apk")[0], json_datas1)
    write_data_to_file(u"非首次启动总耗时", device_name, getApkName().split(".apk")[0], json_datas2)
    write_data_to_file(u"首次启动总耗时", device_name, getApkName().split(".apk")[0] + "_launch", launching_datas1)
    write_data_to_file(u"非首次启动总耗时", device_name, getApkName().split(".apk")[0] + "_launch", launching_datas2)

    create_sheet(json_detail, dict1, json_detail2, dict2, device_name)

    # 还差一个画折线图

    end_time = datetime.datetime.now()
    MLog.info("all time = {}, video_frame time = {}, calculate time = {}, datacharts time = {}".format(
        end_time - start_time,
        end_video_2_frame_time - start_time,
        end_calculate_time - end_video_2_frame_time,
        end_time - end_calculate_time))


if __name__ == '__main__':
    MLog.debug(u"程序启动...")
    # 取序列号
    start_time = datetime.datetime.now()
    serial = getDevices()
    devices = []
    pool = Pool(len(serial) + 1)  # 取电脑核数
    for index in range(len(serial)):
        serial_numebr = serial[index]
        devices.append(getDeviceInfo(serial_numebr))
        # 好扯啊这个
        pool.apply_async(test_main, args=(serial_numebr,))
    pool.close()
    pool.join()
    # 专门画总图
    create_lines(devices, getApkName())
    #
    sendEmailWithDefaultConfig()  # 发邮件
    end_time = datetime.datetime.now()
    MLog.info("all time = {}".format(end_time - start_time))
    print 1
