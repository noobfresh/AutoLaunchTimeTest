# ecoding=utf-8
import os

from datachart.charts import write_json
from log.log import MLog
from uitl.fileUtil import checkSrcVialdAndAutoCreate

file_path = os.path.dirname(__file__) + os.sep + u"files" + os.sep


# 将计算结果分类存储到各级目录下
def write_data_to_file(type, device, apk, json_data):
    suffix = u".json"
    src = file_path + type + os.sep + device + os.sep
    MLog.debug(u"data_center write_data_to_file:" + src)
    checkSrcVialdAndAutoCreate(src)
    json_file = src + apk + suffix
    MLog.debug(u"data_center write_data_to_file:" + json_file)
    write_json(json_data, json_file)


if __name__ == '__main__':
    json_data = {
        "app": "7.14",
        "datas": [
            2966,
            3166,
            3166,
            3066,
            2833,
            2900,
            3066,
            3033
        ]
    }
    write_data_to_file(u"首次启动总耗时", u"Vivo_X9", u"7.14", json_data)
