# encoding: utf-8
import json
import os

from pyecharts import Line, Page, Style

from log.log import MLog

file_path = os.path.dirname(__file__) + os.sep + "dataresult" + os.sep


# 代码一幅图
class ChartItem:
    def __init__(self, title, json_data, show_avg=False):
        self.title = title
        self.json_data = json_data
        self.show_avg = show_avg


# 代表一条线
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


# 创建一幅图
def create_charts(result_name, chart_items):
    lines = []
    json_file_name = 'chart_data.json'
    for item in chart_items:
        lines.append(create_line_by_json(json_file_name, item.title))

    create_page(lines, result_name)


# 创建网页,.html
def create_page(lines, result_file_name):
    page = Page()

    for line in lines:
        page.add(line)

    file_name = file_path + result_file_name + ".html"
    MLog.debug(u"create_page: 开始生成图表...")
    MLog.debug(u"create_page: 图表生成路径:" + file_name)

    try:
        if not os.path.exists(file_path):
            MLog.debug(u"create_page: 目录不存在，现在创建一个...")
            os.mkdir(file_path)

    except Exception, e:
        MLog.error(u"create_page: 创建文件失败！，异常如下:" + repr(e))
    finally:
        page.render(file_name.decode('utf-8'))


def create_line(title, line_data, show_avg):
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

    for data in line_data:
        if show_avg is True:
            chart.add(data.phone_type, attr, data.dataList, is_label_show=True, mark_line=["average"])
        else:
            chart.add(data.phone_type, attr, data.dataList, is_label_show=True)
    return chart


def create_line_by_json(json_file_name, title, show_avg=False):
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

    return create_line(title, line_data, show_avg)


def main():
    json_data = "data.json"
    title = "title"
    create_line_by_json(json_data, title)


if __name__ == '__main__':
    main()
