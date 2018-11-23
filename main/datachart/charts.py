# encoding: utf-8
import json
import os

from pyecharts import Line, Page, Style

file_path = os.path.dirname(__file__) + os.sep + "dataresult" + os.sep


class ChartItem:

    def __init__(self, title, json_data):
        self.title = title
        self.json_data = json_data


class LineData:
    def __init__(self, data, phone_type):
        self.phone_type = phone_type
        self.dataList = data


def utf8(file_name):
    return file_name.decode('utf-8')


def write_json(json_data, json_file_name):
    fileObject = open(json_file_name, 'w')
    fileObject.write(json.dumps(json_data))
    fileObject.close()


def create_charts(result_name, chart_items):
    lines = []
    json_file_name = 'chart_data.json'
    for item in chart_items:
        write_json(item.json_data, json_file_name)
        lines.append(create_line_by_json(json_file_name, item.title))

    create_page(lines, result_name)


def create_page(lines, result_file_name):
    page = Page()

    for line in lines:
        page.add(line)

    file_name = file_path + result_file_name + ".html"

    print u"开始生成图表..."
    print u"图表生成路径:" + file_name
    page.render(file_name.decode('utf-8'))


def create_line(title, line_data):
    # 横竖坐标的大小
    style = Style(
        width=800, height=600
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
    return chart


def create_line_by_json(json_file_name, title):
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

    return create_line(title, line_data)


def main():
    # 生成折线图
    json_datas = [{"app": "7.11", "datas": [8266.67, 6233.33, 7300, 7266.67, 6766.67]},
                  {"app": "7.12", "datas": [5600, 5366.67, 5466.67, 5133.33, 4966.67]}]
    result_name = "chart"
    chart1 = ChartItem("折线图样本实例", json_datas)
    chart2 = ChartItem("折线图样本实例", json_datas)
    chart_items = [chart1, chart2]
    create_charts(result_name, chart_items)
    chart_items = [chart1, chart2]


if __name__ == '__main__':
    main()
