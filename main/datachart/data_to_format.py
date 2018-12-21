# encoding: utf-8
import collections
import json
import os

from calculate.conclude import multi_huya_calculate, multi_normal_calculate
from config.configs import Config
from config.sys_config import get_device_params, get_start_params, getApkName
from datachart.data_center import write_data_to_file
from datachart.data_transform import json_file_to_type
from datachart.handledata import create_detail_sheet_by_json
from log.log import MLog


# 去掉最低最高取平均
from uitl.baseUtil import utf8


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


def format_data(first_launch_result, normal_launch_result, apk_name):

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

    print apk_name + "   *****************************"
    json_datas1 = {
        "app": apk_name,
        "datas": total_datas1
    }

    json_datas2 = {
        "app": apk_name,
        "datas": total_datas2
    }

    json_launching1 = {
        "app": apk_name + u"_launching",
        "datas": launching_datas1
    }

    json_launching2 = {
        "app": apk_name + u"_launching",
        "datas": launching_datas2
    }

    # write log data
    MLog.info(json.dumps(json_datas1))
    MLog.info(json.dumps(json_datas2))
    MLog.info(json.dumps(json_detail))
    MLog.info(json.dumps(json_detail2))
    MLog.info(json.dumps(dict1))
    MLog.info(json.dumps(dict2))
    return json_datas1, json_datas2, json_detail, dict1, json_detail2, dict2, json_launching1, json_launching2


def create_charts(json_datas1, json_datas2):
    device_name = get_device_params()
    apk_name = getApkName()

    MLog.info(json.dumps(json_datas1))
    MLog.info(json.dumps(json_datas2))
    write_data_to_file(u"首次启动总耗时", device_name, apk_name, json_datas1)
    write_data_to_file(u"非首次启动总耗时", device_name, apk_name, json_datas2)


def create_sheet(json_detail, dict1, json_detail2, dict2, device_name):
    apk_name = getApkName()

    sheet_name = device_name + "_detail_time_cost"
    file_name = device_name + "_data_detail"

    MLog.info(u"data_to_format create_sheet:-----------------" )
    MLog.info(json.dumps(json_detail))
    MLog.info(json.dumps(dict1))
    create_detail_sheet_by_json(sheet_name, file_name, device_name + " " + apk_name + u" 耗时统计", json_detail, dict1)
    print "--------------------------------------------------------"

    MLog.info(json.dumps(json_detail2))
    MLog.info(json.dumps(dict2))
    print "--------------------------------------------------------"
    create_detail_sheet_by_json(sheet_name, "data_result", device_name + " " + apk_name + u" 平均耗时统计",
                                json_detail2, dict2)


def create_lines(devices, apk_name):
    types = [u"非首次启动总耗时", u"首次启动总耗时"]
    apk_name = "71416"
    apks = [utf8(apk_name), utf8(apk_name) + u"_launch"]
    json_file_to_type(types, devices, apks)
    MLog.info("create_lines done!")


if __name__ == '__main__':
    create_lines(["PACM00"], "")
