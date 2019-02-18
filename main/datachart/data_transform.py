# encoding: utf-8
import os

from datachart.charts import create_charts, ChartItem
from log.log import MLog

from uitl.baseUtil import read_json, list2str
from uitl.fileUtil import fileExist, count_file

json_file_path = os.path.dirname(__file__) + os.sep + "files" + os.sep


def get_json_file(type, device, apk):
    apk = apk.replace(u".apk", '')
    return json_file_path + os.sep + type + os.sep + device + os.sep + apk + ".json"


# 根据指定类型将所有该类型下的数据全部生成
# types：类型  | devices：设备名  | apk：app名
def json_file_to_type(types, devices, apks):
    MLog.info(u"data_transform :打印传入的参数  ")
    MLog.info(u"data_transform json_file_to_type:"
              u"apks = " + list2str(apks) + u" devices = " + list2str(devices) + u" types = " + list2str(types))
    result_name = u"chart"
    lines = []
    for type in types:
        src = json_file_path + type
        if fileExist(src):
            for device in devices:
                new_src = src + os.sep + device
                if fileExist(new_src):
                    if count_file(new_src, u".json") > 0:
                        lines.append(json_file_to_charts(type, device, apks))

    if len(lines) == 0:
        MLog.error(u"收集到的折线为0，直接返回!")
        return
    create_charts(result_name, lines)


#  生成一副折线图，给外部调用
def json_file_to_charts(type, device, apks):
    MLog.info(u"json_file_to_charts: type = " + type + u", device = " + device + u", apks =" + str(apks))
    MLog.debug(u"json_file_to_charts: 开始生成折线图...")
    lines = []
    for apk in apks:
        file = get_json_file(type, device, apk)
        try:
            MLog.debug(u"尝试打开文件file: " + file)
            if not fileExist(file):
                continue
            lines.append(read_json(file))
        except Exception, e:
            MLog.error(u"打开文件失败" + file)
            MLog.error(u"e = " + repr(e))
            print lines
    # MLog.debug(u"json_file_to_charts: 生成折线图完成...")
    # MLog.info(u"------------------折线图生成异常请看下面折线数量是否大于0-----------------")
    MLog.info(u"json_file_to_charts: 生成折线数量 = " + str(len(lines)))
    return ChartItem(device + type, lines)


# 通过每幅图的file.json文件生成图表，src代表目录
def create_from_file_per(src, title, show_avg):
    MLog.debug(u"data_transform create_from_file_per: 通过读取json文件生成图表数据")

    # 子目录或文件
    lst = []
    for item in os.listdir(src):
        item = item.decode('GB2312')
        path = os.path.join(src, item)
        if os.path.splitext(path)[1] == '.json':
            lst.append(path)
            MLog.debug(u"create_from_file_per: add path " + path)

    lines = []
    chart_items = []
    result_name = "chart"
    for file in lst:
        MLog.debug(u"create_from_file_per: file = " + file)
        lines.append(read_json(file))
    print lines

    file_name = title
    chart = ChartItem(file_name, lines, show_avg)
    chart_items.append(chart)
    create_charts(result_name, chart_items)


if __name__ == '__main__':
    types = [u"非首次启动总耗时", u"首次启动总耗时", u"进直播间耗时", u"非首次启动闪屏页耗时", u"首次启动闪屏页耗时"]
    devices = [u"OPPOA83", u"vivoX9", u"MiNote2", u"PACM00"]
    apks = [u"7.15"]  ## 具体来说apks就是代表图中的折线!!!

    # 生成当前type下所有,所有机型指定apks的图表
    json_file_to_type(types, devices, apks)

    # 生成指定type,指定机型，指定apks的图表
    # json_file_to_charts(type, device, apks)

    # create_chart_from_file()
