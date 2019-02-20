# encoding: utf-8
import collections
import json
import os

from config.sys_config import getApkName
from datachart.data_center import write_data_to_file
from datachart.data_transform import json_file_to_type
from datachart.handledata import create_detail_sheet_by_json
from log.log import MLog

from uitl.baseUtil import utf8, write_json
from uitl.fileUtil import checkSrcVialdAndAutoCreate

file_path = os.path.dirname(__file__) + os.sep + "files" + os.sep + u"表格数据" + os.sep


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


def format_data(first_launch_result, normal_launch_result, enter_ent, apk_name):
    # 算平均值啥的
    total_datas1 = []
    launching_datas1 = []
    homepage_datas1 = []
    ent_live_room_result = []
    for x, y, z in enter_ent:
        print(x, y, z)
        cost = (z - x + 1) * 20
        ent_live_room_result.append(cost)

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

    detail_data = []
    max_count = max(len(total_datas1), len(total_datas2), len(ent_live_room_result))
    for i in range(1, max_count + 1):
        dict_temp = collections.OrderedDict()
        dict_temp[u"次数"] = str(i)
        dict_temp[u"首次启动总耗时"] = checkVaild(launching_datas1, i - 1)
        dict_temp[u"首次启动首页加载耗时"] = checkVaild(homepage_datas1, i - 1)
        dict_temp[u"非首次启动总耗时"] = checkVaild(total_datas2, i - 1)
        dict_temp[u"非首次启动耗时"] = checkVaild(launching_datas2, i - 1)
        dict_temp[u"非首次启动首页加载耗时"] = checkVaild(homepage_datas2, i - 1)
        dict_temp[u"进入直播间耗时"] = checkVaild(ent_live_room_result, i - 1)
        detail_data.append(dict_temp)
    MLog.info(u"Excel表格耗时详细数据")
    MLog.info(json.dumps(detail_data, ensure_ascii=False).decode('utf8'))

    avg_detail_data = []
    dict_avg = {
        u"平均首次启动总耗时": avg_list(total_datas1),
        u"平均首次启动耗时": avg_list(launching_datas1),
        u"平均首次启动首页加载耗时": avg_list(homepage_datas1),
        u"平均非首次启动总耗时": avg_list(total_datas2),
        u"平均非首次启动耗时": avg_list(launching_datas2),
        u"平均非首次启动首页加载耗时": avg_list(homepage_datas2)}
    avg_detail_data.append(dict_avg)
    MLog.info(u"Excel表格平均耗时详细数据")
    MLog.info(json.dumps(avg_detail_data, ensure_ascii=False).decode('utf8'))

    first_launch_all_datas = {
        "app": apk_name,
        "datas": total_datas1
    }

    normal_launch_all_datas = {
        "app": apk_name,
        "datas": total_datas2
    }

    first_lunch_splash_datas = {
        "app": apk_name + u"_launching",
        "datas": launching_datas1
    }

    normal_launch_splash_datas = {
        "app": apk_name + u"_launching",
        "datas": launching_datas2
    }

    enter_liveroom_datas = {
        "app": getApkName().split(".apk")[0],
        "datas": ent_live_room_result
    }
    return first_launch_all_datas, normal_launch_all_datas, detail_data, avg_detail_data, first_lunch_splash_datas, normal_launch_splash_datas, enter_liveroom_datas


def checkVaild(datas, index):
    if datas == [] or index >= len(datas):
        return u"暂无数据"
    else:
        return str(datas[index])


def create_sheet(json_detail_data, json_avg_detail, device_name):
    MLog.info(u"--------------------------开始准备生成表格---------------------------")
    MLog.info(u"data_to_format create_sheet:创建表格开始...")
    apk_name = getApkName()
    sheet_name = device_name + "_detail_time_cost"
    file_name = device_name + "_data_detail"
    checkSrcVialdAndAutoCreate(file_path)
    write_json(json_detail_data, file_path + 'alldata.json')
    write_json(json_avg_detail, file_path + 'avgdata.json')

    MLog.info(u"创建耗时统计 -> json数据文件为json_detail_data: ")
    MLog.info(json.dumps(json_detail_data, ensure_ascii=False).decode('utf8'))
    title = device_name + " " + apk_name + u" 耗时统计"
    create_detail_sheet_by_json(sheet_name, file_name, title, json_detail_data)

    MLog.info(u"创建平均耗时统计 -> json数据文件为json_avg_detail: ")
    MLog.info(json.dumps(json_avg_detail, ensure_ascii=False).decode('utf8'))
    title = device_name + " " + apk_name + u" 平均耗时统计"
    create_detail_sheet_by_json(sheet_name, "avg_data_result", title, json_avg_detail)
    MLog.info(u"--------------------------生成表格结束---------------------------")


def create_lines(devices, apk_name):
    MLog.info(u"--------------------------开始准备生成折线图---------------------------")
    types = [u"非首次启动总耗时", u"首次启动总耗时", u"进直播间耗时", u"非首次启动闪屏页耗时", u"首次启动闪屏页耗时"]
    apks = [utf8(apk_name)]
    json_file_to_type(types, devices, apks)
    MLog.info(u"--------------------------生成折线图结束---------------------------")


def write_data_local(device_name, enter_liveroom_datas, first_launch_all_datas, first_lunch_splash_datas,
                     normal_launch_all_datas, normal_launch_splash_datas):
    # write log data
    MLog.info(u"--------------------------开始写入json数据到本地--------------------------")
    MLog.debug(u"首次启动总耗时->")
    MLog.info(json.dumps(first_launch_all_datas, ensure_ascii=False).decode('utf8'))
    MLog.debug(u"非首次启动总耗时>")
    MLog.info(json.dumps(normal_launch_all_datas, ensure_ascii=False).decode('utf8'))
    MLog.debug(u"首次启动闪屏页耗时->")
    MLog.info(json.dumps(first_lunch_splash_datas, ensure_ascii=False).decode('utf8'))
    MLog.debug(u"非首次启动闪屏页耗时->")
    MLog.info(json.dumps(normal_launch_splash_datas, ensure_ascii=False).decode('utf8'))
    MLog.debug(u"进直播间耗时->")
    MLog.info(json.dumps(enter_liveroom_datas, ensure_ascii=False).decode('utf8'))
    # 写 JSON 数据
    write_data_to_file(u"首次启动总耗时", device_name, getApkName().split(".apk")[0], first_launch_all_datas)
    write_data_to_file(u"非首次启动总耗时", device_name, getApkName().split(".apk")[0], normal_launch_all_datas)
    write_data_to_file(u"首次启动闪屏页耗时", device_name, getApkName().split(".apk")[0], first_lunch_splash_datas)
    write_data_to_file(u"非首次启动闪屏页耗时", device_name, getApkName().split(".apk")[0], normal_launch_splash_datas)
    write_data_to_file(u"进直播间耗时", device_name, getApkName().split(".apk")[0], enter_liveroom_datas)
    MLog.info(u"--------------------------写入json数据到本地结束--------------------------")


if __name__ == '__main__':
    device_name = "test_device"
    sheet_name = device_name + "_detail_time_cost"
    file_name = device_name + "_data_detail"
    apk_name = "7.16.apk"
    json_detail = [
        {"次数": "1", "首次启动总耗时": "3700", "首次启动首页加载耗时": "360", "非首次启动总耗时": "3340", "非首次启动耗时": "2840", "非首次启动首页加载耗时": "500",
         "进入直播间耗时": "暂无数据"},
        {"次数": "2", "首次启动总耗时": "3300", "首次启动首页加载耗时": "380", "非首次启动总耗时": "3140", "非首次启动耗时": "2760", "非首次启动首页加载耗时": "380",
         "进入直播间耗时": "暂无数据"},
        {"次数": "3", "首次启动总耗时": "3340", "首次启动首页加载耗时": "360", "非首次启动总耗时": "3120", "非首次启动耗时": "2720", "非首次启动首页加载耗时": "400",
         "进入直播间耗时": "暂无数据"}]

    create_detail_sheet_by_json(sheet_name, file_name, device_name + " " + apk_name + u" 耗时统计", json_detail)
