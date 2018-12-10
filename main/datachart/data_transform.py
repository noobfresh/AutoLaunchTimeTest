# encoding: utf-8
import json
import os

from datachart.charts import create_charts, ChartItem
from log.log import MLog

json_file_path = os.path.dirname(__file__) + os.sep + "files" + os.sep


def get_json_file(type, device, apk):
    return json_file_path + os.sep + type + os.sep + device + os.sep + apk + ".json"


# 根据指定类型将所有该类型下的数据全部成
def json_file_to_type(types, apks):
    result_name = u"chart"
    devices = []

    for type in types:
        src = json_file_path + type
        if not os.path.exists(src):
            MLog.error(u"文件夹: '" + type + u"' 不存在!")
            return

        lines = []
        for item in os.listdir(src):
            device = item.decode('GB2312')
            devices.append(device)
            MLog.debug(u"json_file_to_type:" + u"add :" + device)
            lines.append(json_file_to_charts(type, device, apks))

    create_charts(result_name, lines)


#  指定同一台机型比较下比较那几个apk
def json_file_to_charts(type, device, apks):
    MLog.info(u"json_file_to_charts: type = " + type + u", device = " + device + u", apks =" + str(apks))
    MLog.debug(u"json_file_to_charts:" + u"开始生成折线图...")
    lines = []
    for apk in apks:
        file = get_json_file(type, device, apk)
        try:
            MLog.debug(u"尝试打开文件file: " + file)
            with open(file, 'r') as f:
                line = json.load(f)
                lines.append(line)
        except Exception, e:
            MLog.error(u"打开文件失败" + file)
            MLog.error(u"e = " + repr(e))

            print lines
    return ChartItem(device + type, lines)


if __name__ == '__main__':

    device = u"Oppo_A37"
    type = [u"非首次启动总耗时"]
    apks = [u"7.11", u"7.12", u"7.14"]

    # 生成当前type下所有,所有机型指定apks的图表
    json_file_to_type(type, apks)

    # 生成指定type,指定机型，指定apks的图表
    # json_file_to_charts(type, device, apks)
