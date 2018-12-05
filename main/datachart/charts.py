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


def create_from_file():
    print u"通过读取json文件生成图表数据..."

    lst = []
    src = os.path.dirname(__file__) + os.sep + "jsonfile"
    for item in os.listdir(src):
        item = item.decode('GB2312')
        path = os.path.join(src, item)
        if os.path.splitext(path)[1] == '.json':
            lst.append(path)
            print "add " + path

    chart_items = []
    result_name = "chart"
    for file in lst:
        with open(file, 'r') as load_f:
            data = json.load(load_f)
            base_name = os.path.basename(file)
            # 去掉后缀
            file_name = os.path.splitext(base_name)[0]
            chart = ChartItem(file_name, data)
            chart_items.append(chart)

    create_charts(result_name, chart_items)


def create_by_json():

    # 生成折线图
    a83_json_data1 = [{"app": "7.11", "datas": [14500, 13266, 12600, 12633, 12300, 11333, 12166, 11700]},
                      {"app": "7.12", "datas": [11366, 11533, 11100, 9500, 10933, 10700, 10566, 11400]},
                      {"app": "7.14", "datas": [4866, 4733, 4600, 4800, 4633, 4800, 4766, 4566]},
                      {"app": "huya", "datas": [6966, 6566, 5933, 5833, 7166, 7400, 5800, 7133]}]

    a83_json_data2 = [{"app": "7.11", "datas": [8600, 9066, 8233, 8200, 9533, 8400, 8300, 8400]},
                      {"app": "7.12", "datas": [8200, 7666, 7000, 7866, 7900, 7233, 7366, 7466]},
                      {"app": "7.14", "datas": [2380, 2380, 2360, 2380, 2360, 2340, 2380, 2380]},
                      {"app": "huya", "datas": [1633, 1700, 1600, 1666, 1733, 1633, 1633, 1666]}]

    a83_json_data3 = [{"app": "7.11", "datas": [133, 133, 133, 134, 200, 134, 133, 133]},
                      {"app": "7.12", "datas": [133, 167, 167, 133, 134, 167, 200, 166]},
                      {"app": "7.14", "datas": [200, 166, 200, 200, 167, 167, 166, 167]},
                      {"app": "huya", "datas": [200, 166, 300, 200, 333, 166, 200, 200]}
                      ]

    phone = "红米5Plus"
    result_name = "chart"
    chart1 = ChartItem(phone + "首次启动总耗时", a83_json_data1)
    chart2 = ChartItem(phone + "非首次启动总耗时", a83_json_data2)
    chart3 = ChartItem(phone + "首页加载耗时", a83_json_data3)
    chart_items = [chart1, chart2, chart3]

    create_charts(result_name, chart_items)


def main():
    create_from_file()


if __name__ == '__main__':
    main()
