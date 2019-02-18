# ecoding=utf-8
import collections
import os

from pyExcelerator import *

from log.log import MLog
from uitl.fileUtil import checkSrcVialdAndAutoCreate

reload(sys)
sys.setdefaultencoding('utf-8')

file_path = os.path.dirname(__file__) + os.sep + "dataresult" + os.sep


def init_normal_style():
    style = XFStyle()
    style.font.name = 'Times New Roman'
    style.font.struck_out = True
    style.font.bold = True
    style.font.outline = True

    # 这里设置边框
    borders = Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1

    # 这里设置对齐方式
    al = Alignment()
    al.horz = Alignment.HORZ_CENTER
    al.vert = Alignment.VERT_CENTER

    style = XFStyle()
    style.borders = borders
    style.alignment = al
    return style


# 创建详细数据excel表格
def create_detail_sheet_by_json(sheet_name, file_name, title, json_data, title_list):
    if json_data is None or json_data is [] or len(json_data) == 0:
        MLog.error(u"json == None or json_data == [], return !")
        raise Exception(u"Invalid json_data! json_data is None")
    if len(json_data[0].keys()) != len(title_list):
        MLog.error(u"title's len ! = jsondata[0].keys() ,return!")
        raise Exception(u"Invalid args! title's length need equls jsondata[0].keys() length")

    # 创建一个工作簿
    w = Workbook()
    # 创建一个工作表
    ws = w.add_sheet(sheet_name)
    style = init_normal_style()

    # 调整单元格宽度，先调20个够用
    content_size = 6000
    for i in range(0, 20):
        ws.col(i).width = content_size

    # 表格偏移量
    x_offset = 0
    y_offset = 0

    MLog.debug(str(json_data))

    ws.write_merge(y_offset, y_offset, x_offset, x_offset + len(json_data[0]) - 1, unicode(str(title), 'utf-8'), style)

    for index in range(0, len(json_data)):
        cur = 0
        for key, value in title_list.items():
            if index == 0:
                # 写标题
                ws.write(y_offset + 1, x_offset + cur, title_list[key], style)
            # 写内容
            ws.write(index + y_offset + 2, x_offset + cur, json_data[index][key], style)
            cur += 1

    file_name = file_path + file_name

    checkSrcVialdAndAutoCreate(file_path)
    w.save(file_name + '.xls')
    MLog.debug(u"handledata create_detail_sheet_by_json: Excel文件生成路径:" + os.path.abspath(file_name))


def transform():
    print u"将数据装换成任意你想要的"


def main():
    file_name = u"耗时详情"
    sheet_name = "detail_time_cost"
    title = u"oppo r11 耗时统计"

    json_detail = [
        {"count": "1", "first_start": "4444", "normal_start": "3333", "home_start": "4444"},
        {"count": "2", "first_start": "4444", "normal_start": "3333", "home_start": "4444"},
        {"count": "3", "first_start": "4444", "normal_start": "3333", "home_start": "4444"},
    ]

    title_list = {"count": u"次数", "first_start": u"首次启动耗时", "normal_start": u"非首次启动耗时", "home_start": u"首页耗时"}

    create_detail_sheet_by_json(sheet_name, file_name, title, json_detail, title_list)

    ############# 下面是平均耗时
    file_name = u"平均结果"
    data = [{"first_start": "7.17", "phone": "OPPO R9s", "app": "7.11.1", "home": "0.15", "normal_start": "5.65"},
            {"first_start": "7.17", "phone": "OPPO R9s", "app": "7.11.1", "home": "0.15", "normal_start": "5.65"}]

    # title_list2 = {"phone": u"机型", "app": u"应用", "first_start": u"非首次启动耗时", "normal_start": u"首次启动", "home": u"首页加载"}

    d1 = collections.OrderedDict()  # 将普通字典转换为有序字典
    d1['phone'] = u"机型"
    d1['app'] = u"应用"
    d1['first_start'] = u"非首次启动耗时"
    d1['normal_start'] = u"首次启动"
    d1['home'] = u"首页耗时"

    create_detail_sheet_by_json(sheet_name, file_name, title, data, d1)


if __name__ == '__main__':
    main()
