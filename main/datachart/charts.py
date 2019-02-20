# encoding: utf-8
import os

from pyecharts import Line, Page, Style

from log.log import MLog
from uitl.baseUtil import read_json
from uitl.fileUtil import checkSrcVialdAndAutoCreate

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


# 创建一幅图
def create_charts(result_name, chart_items):
    lines = []
    for item in chart_items:
        lines.append(create_line_by_param(item.json_data, item.title))

    if len(lines) > 0:
        create_page(lines, result_name)


# 创建网页,.html
def create_page(lines, result_file_name):
    page = Page()

    for line in lines:
        if line is not None:
            page.add(line)

    file_name = file_path + result_file_name + ".html"
    MLog.info(u"create_page: 开始生成图表...")
    MLog.info(u"create_page: 图表包含的折线图数量为:" + str(len(page)))
    MLog.info(u"create_page: 图表生成路径:" + file_name)

    checkSrcVialdAndAutoCreate(file_path)
    page.render(file_name.decode('utf-8'))


# 创建真正图中的线
def create_line(title, line_data, show_avg=True, attr=None):
    # 横竖坐标的大小
    style = Style(
        width=800, height=600
    )

    chart = Line(title, **style.init_style)

    if len(line_data) == 0:
        return

    if attr is None:
        attr = []
        size = len(line_data[0].dataList)
        for i in range(1, size + 1):
            cur = u"第 " + str(i) + u" 次"
            attr.append(cur)

    for data in line_data:
        if show_avg is True:
            chart.add(data.phone_type, attr, data.dataList, is_label_show=True, mark_line=["average"])
        else:
            chart.add(data.phone_type, attr, data.dataList, is_label_show=True)
    return chart


# 直接通过传入json_object创建折线
def create_line_by_param(json_object, title, show_avg=False):
    line_data = []
    for data in json_object:
        v = data['datas']
        app = data['app']
        line = LineData(v, app)
        line_data.append(line)

    return create_line(title, line_data, show_avg)


# 通过读取json文件创建折线
def create_line_by_json(json_file_name, title, show_avg=False):
    if not os.path.exists(json_file_name):
        print u"json 文件读取失败! ," + json_file_name + u"不存在"
        return

    return create_line_by_param(read_json(json_file_name), title, show_avg)


def main():
    json_data = "data.json"
    title = "title"
    result_file_name = "test"
    lines = []
    lines.append(create_line_by_json(json_data, title))
    create_page(lines, result_file_name)


if __name__ == '__main__':
    main()
