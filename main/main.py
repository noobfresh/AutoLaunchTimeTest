# coding=utf-8
import datetime
import time
from multiprocessing import Pool

import settings
from calculate.conclude import start_calculate
from config.sys_config import get_start_params, getApkName
from datachart.charts import *
from datachart.data_to_format import format_data, create_sheet, create_lines, write_data_local
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
    MLog.debug("first_launch_result ==========")
    MLog.debug(first_launch_result)
    MLog.debug("normal_launch_result ==========")
    MLog.debug(normal_launch_result)
    MLog.debug("enter ent ==========")
    MLog.debug(enter_ent)

    first_launch_all_datas, normal_launch_all_datas, detail_data, avg_detail_data, first_lunch_splash_datas, normal_launch_splash_datas, enter_liveroom_datas = format_data(
        first_launch_result,
        normal_launch_result,
        enter_ent,
        apkName)
    end_calculate_time = datetime.datetime.now()
    MLog.info(u"计算时间 time ={}".format(end_calculate_time - end_video_2_frame_time))

    # ---------------------------- UI Part ------------------------------#
    # 创建表格
    create_sheet(detail_data, avg_detail_data, device_name)
    # 写入json数据到本地
    write_data_local(device_name, enter_liveroom_datas, first_launch_all_datas, first_lunch_splash_datas,
                     normal_launch_all_datas, normal_launch_splash_datas)

    end_time = datetime.datetime.now()
    MLog.info("all time = {}, video_frame time = {}, calculate time = {}, datacharts time = {}".format(
        end_time - start_time,
        end_video_2_frame_time - start_time,
        end_calculate_time - end_video_2_frame_time,
        end_time - end_calculate_time))


def start():
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
        # pool.apply_async(test_main, args=(serial_number,))
        # 下面方法注释开会导致进程阻塞，debug时可以打开，运行时注释掉！！！
        result = pool.apply_async(test_main, args=(serial_number,))
        result.get()
    pool.close()
    pool.join()
    # 生成图表
    create_lines(devices, getApkName())

    # sendEmailWithDefaultConfig()  # 发邮件
    end_time = datetime.datetime.now()
    MLog.info("all time = {}".format(end_time - start_time))
    MLog.info(u"end main...")


def startAppWithConfig(params):
    '''
       带参数的启动方式
    '''
    MLog.debug(u"main startAppWithConfig:" + params.sdk_path)
