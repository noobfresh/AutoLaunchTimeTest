# encoding: utf-8
import json
import os

from pyecharts import Line, Page, Style

# file_path = os.getcwd() + '\\' + os.path.join('dataresult', '')
file_path = 'C:\\Users\\Administrator\\PycharmProjects\\AutoLaunchTimeTest\\main\\datachart\\dataresult\\'


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
    print line_data

    size = line_data[0].dataList.__len__()
    print "len = " + str(size)
    for i in range(1, size + 1):
        cur = "第 " + str(i) + " 次"
        attr.append(cur)

    print attr
    # print (title)

    for data in line_data:
        # print (data.phone_type)
        # print (data.dataList)
        chart.add(data.phone_type, attr, data.dataList, is_label_show=True)
    page.add(chart)

    return page


def create_line(json_file_name, title, result_file_name):
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

    print "开始生成柱状图..."
    print "柱状图生成路径:" + file_name
    create_charts(title, line_data).render(file_name.decode('utf-8'))


def main():
    json_file_name = "datas.json"
    phone_type = "oppo r9s"
    title = phone_type + "首次启动耗时"
    result_file_name = str("cheart").decode('utf-8')
    create_line(json_file_name, title, result_file_name)


if __name__ == '__main__':
    main()
