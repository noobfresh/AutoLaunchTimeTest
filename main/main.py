# coding=utf-8
import datetime
from multiprocessing import Pool
import time

import settings
from calculate import first_frame_calculate
from calculate.conclude import start_calculate
from config.sys_config import get_start_params, getApkName
from datachart.charts import *
from datachart.data_center import write_data_to_file
from datachart.data_to_format import format_data, create_sheet, create_lines
from datachart.sendmail import sendEmailWithDefaultConfig
from log.log import MLog
from screenrecord.device_info import getDeviceInfo
from screenrecord.screen_record_main import start_python, getDevices
from uitl import dbutil


def testdb():
    dbutil.connect("datas.db")
    # dbutil.create("detail",
    #               {"device": "text", "time": "text", "first_all_cost": "TEXT", "first_splash_cost": "TEXT",
    #                "first_homepage_cost": "TEXT", "normal_all_cost": "TEXT", "normal_splash_cost": "TEXT",
    #                "normal_homepage_cost": "TEXT", "enter_live_room_cost": "TEXT"})
    dbutil.insert("detail",
                  {"device": "text", "time": "text", "first_all_cost": "TEXT", "first_splash_cost": "TEXT",
                   "first_homepage_cost": "TEXT", "normal_all_cost": "TEXT", "normal_splash_cost": "TEXT",
                   "normal_homepage_cost": "TEXT", "enter_live_room_cost": "TEXT"})
    dbutil.close()


def test_main(serial_num):
    settings._init()
    firstLaunchTimes, notFirstLaunchTimes, enterLiveTimes, apkName = get_start_params()
    MLog.info("current Device = {}".format(serial_num))
    start_time = datetime.datetime.now()
    start_python(firstLaunchTimes, notFirstLaunchTimes, enterLiveTimes, apkName, serial_num)
    end_video_2_frame_time = datetime.datetime.now()
    MLog.info(u"录屏及切帧时间 time = {}".format(end_video_2_frame_time - start_time))

    path = os.path.dirname(__file__) + "\\"
    os.chdir(path)
    print path
    device_name = getDeviceInfo(serial_num)
    first_launch_result, normal_launch_result, enter_ent = start_calculate(device_name)
    print " enter_ent -> {}".format(enter_ent)
    MLog.debug(first_launch_result)
    MLog.debug(normal_launch_result)

    ent_live_room_result = []
    for x, y, z in enter_ent:
        print(x, y, z)
        cost = (z - x + 1) * 20
        ent_live_room_result.append(cost)

    json_entliveroom = {
        "app": getApkName().split(".apk")[0],
        "datas": ent_live_room_result
    }

    json_datas1, json_datas2, json_detail, dict1, json_detail2, dict2, launching_datas1, launching_datas2 = format_data(
        first_launch_result,
        normal_launch_result,
        ent_live_room_result,
        apkName)
    end_calculate_time = datetime.datetime.now()
    MLog.info(u"计算时间 time ={}".format(end_calculate_time - end_video_2_frame_time))

    # ---------------------------- UI Part ------------------------------#
    MLog.info(u"开始写表格...")
    create_sheet(json_detail, dict1, json_detail2, dict2, device_name)

    MLog.info(u"开始写json数据...")
    # 写 JSON 数据
    write_data_to_file(u"首次启动总耗时", device_name, getApkName().split(".apk")[0], json_datas1)
    write_data_to_file(u"非首次启动总耗时", device_name, getApkName().split(".apk")[0], json_datas2)
    write_data_to_file(u"首次启动闪屏页耗时", device_name, getApkName().split(".apk")[0], launching_datas1)
    write_data_to_file(u"非首次启动闪屏页耗时", device_name, getApkName().split(".apk")[0], launching_datas2)
    write_data_to_file(u"进直播间耗时", device_name, getApkName().split(".apk")[0], json_entliveroom)

    # 还差一个画折线图

    end_time = datetime.datetime.now()
    MLog.info("all time = {}, video_frame time = {}, calculate time = {}, datacharts time = {}".format(
        end_time - start_time,
        end_video_2_frame_time - start_time,
        end_calculate_time - end_video_2_frame_time,
        end_time - end_calculate_time))


if __name__ == '__main__':
    MLog.debug(u"程序启动...")
    os.system("python -m uiautomator2 init")
    time.sleep(10)
    # 取序列号
    start_time = datetime.datetime.now()
    serial = getDevices()
    MLog.info(u"读取到的序列号 = " + str(serial))
    devices = []
    pool = Pool(len(serial) + 1)  # 取电脑核数
    for index in range(len(serial)):
        serial_number = serial[index]
        MLog.info(u"启动一个新进程 : index = " + str(index) + u" serial_number = " + serial_number)
        devices.append(getDeviceInfo(serial_number))
        pool.apply_async(test_main, args=(serial_number,))
        # 下面方法注释开会导致进程阻塞，debug时可以打开，运行时注释掉！！！
        # result = pool.apply_async(test_main, args=(serial_numeber,))
        # result.get()
    pool.close()
    pool.join()
    # 专门画总图
    create_lines(devices, getApkName())

    # sendEmailWithDefaultConfig()  # 发邮件
    end_time = datetime.datetime.now()
    MLog.info("all time = {}".format(end_time - start_time))
    print u"end main..."
