# ecoding=utf-8
import json
import os

from pyExcelerator import *

import datetime

import sys


reload(sys)
sys.setdefaultencoding('utf-8')

# file_path = os.getcwd() + '\\' + os.path.join('dataresult', '')
file_path = 'E:\\APPstart\\AutoLaunchTimeTest\\main\\datachart\\dataresult\\'

class SheetStruct:

    def __init__(self, phone, app, first_start, start, home):
        self.app = app
        self.phone = phone
        self.home = home
        self.first_start = first_start
        self.start = start


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


def create_sheet_by_json(sheet_name, file_name, list_data):
    # 创建一个工作簿
    w = Workbook()
    # 创建一个工作表
    ws = w.add_sheet(sheet_name)
    # ws.write(2, 4, 'content')  2是行 ，4是列 ，content是内容

    startX = 2
    startY = 1

    title_size = 8000
    content_size = 6000

    ########################################
    style = init_normal_style()
    ws.col(0).width = title_size
    ws.col(1).width = content_size
    ws.col(2).width = content_size
    ws.col(3).width = content_size
    ws.col(4).width = content_size
    #######################################

    titles = ["机型", "版本", "首次启动耗时（s）", "非首次启动耗时（s）"]
    for index in range(0, titles.__len__()):
        ws.write_merge(startY, startY + 1, index, index, unicode(titles[index], 'utf-8'), style)

    ws.write_merge(startY + 2, startY + 2 + list_data.__len__() - 1, 0, 0, list_data[0].phone, style)

    for i in range(0, list_data.__len__()):
        ws.write(startY + i + 2, startX - 1 + 0, list_data[i].app, style)
        ws.write(startY + i + 2, startX - 1 + 1, list_data[i].first_start, style)
        ws.write(startY + i + 2, startX - 1 + 2, list_data[i].start, style)
        # ws.write(startY + i + 2, startX - 1 + 3, list_data[i].home, style)

    file_name = file_path + file_name
    try:
        w.save(file_name + '.xls')
    except :
        new_file_name = file_name + datetime.datetime.now().strftime('_%Y-%m-%d_%H-%M-%S')
        print (file_name + " Excel表格处于打开中，生成名变换为：" + new_file_name)
        w.save(new_file_name + '.xls')
        print ("Excel文件生成路径:" + os.path.abspath(new_file_name))
    else:
        print ("Excel文件生成路径:" + os.path.abspath(file_name))


def create_sheet(sheet_name, file_name, json_file_path):
    with open(json_file_path, 'r') as f:
        # 顺序保证下
        content = f.read()
        text = content.decode("utf-8-sig").encode("utf-8")
        json_object = json.loads(text)

    data_list = []
    print "开始执行写入数据到excel..."
    for data in json_object:
        print data
        item = SheetStruct(data['phone'], data['app'], data['first_start'], data['start'], data['first_start'])
        data_list.append(item)

    create_sheet_by_json(sheet_name, file_name, data_list)


def main():
    sheet_name = "time_cost"
    file_name = "测试结果"
    json_file_path = "data.json"
    create_sheet(sheet_name, file_name.decode('utf-8'), json_file_path)


if __name__ == '__main__':
    main()
