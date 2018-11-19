# encoding: utf-8
import json
import os

from pyecharts import Line, Page, Style

# file_path = os.getcwd() + '\\' + os.path.join('dataresult', '')
file_path = os.path.dirname(__file__) + "\\dataresult\\"


class LineData:
    def __init__(self, data, phone_type):
        self.phone_type = phone_type
        self.dataList = data


def create_charts(title, line_data):
    page = Page()

    # 横竖坐标的大小
    style = Style(
        width=600, height=400
    )

    chart = Line(title, **style.init_style)

    attr = []

    size = line_data[0].dataList.__len__()

    for i in range(1, size + 1):
        cur = u"第 " + str(i) + u" 次"
        attr.append(cur)

    # print (title)

    for data in line_data:
        # print (data.phone_type)
        # print (data.dataList)
        chart.add(data.phone_type, attr, data.dataList, is_label_show=True)
    page.add(chart)

    return page


def create_line(json_file_name, title, result_file_name):
    if not os.path.exists(json_file_name):
        print u"创建表格失败：" + json_file_name + u"不存在"
        return

    with open(json_file_name, 'r') as f:
        # 顺序保证下
        content = f.read()
        text = content.decode("utf-8-sig").encode("utf-8")
        json_object = json.loads(text)

    line_data = []
    for data in json_object:
        v = data['datas']
        app = data['app']
        line = LineData(v, app)
        line_data.append(line)

    file_name = file_path + result_file_name + ".html"

    print u"开始生成图表..."
    print u"图表生成路径:" + file_name
    create_charts(title, line_data).render(file_name.decode('utf-8'))


def main():
    json_file_name = u"datas.json"
    phone_type = u"oppo r9s"
    title = phone_type + u"首次启动耗时"
    result_file_name = str(u"chart").decode('utf-8')
    create_line(json_file_name, title, result_file_name)


if __name__ == '__main__':
    main()
