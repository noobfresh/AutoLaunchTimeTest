# encoding: utf-8

from pyecharts import Line, Page, Style


class LineData:
    def __init__(self, data, phone_type):
        self.phone_type = phone_type
        self.dataList = data


def create_charts(title, line_data, length):
    page = Page()

    # 横竖坐标的大小
    style = Style(
        width=6000, height=400
    )

    # attr = ["第一次", "第二次", "第三次", "第四次", "第五次", "第六次"]
    attr = []
    for i in range(0, length):
        attr.append(str(i))

    chart = Line(title, **style.init_style)

    print (title)

    for data in line_data:
        print (data.phone_type)
        print (data.dataList)
        chart.add(data.phone_type, attr, data.dataList, is_stack=True, is_label_show=True)

    page.add(chart)

    return page


def main():

    v1 = [5, 20, 36, 10, 75, 40]
    v2 = [10, 25, 8, 60, 20, 50]
    v3 = [16, 34, 5, 40, 30, 85]
    v4 = [27, 25, 35, 35, 40, 70]

    attr = ["OPPO r9s", "OPPO r11", "Vivo x20", "Vivo x21a", "Vivo X7", "红米note3"]

    line1 = LineData(v1, attr[1])
    line2 = LineData(v2, attr[2])
    line3 = LineData(v3, attr[3])
    line4 = LineData(v4, attr[4])

    line_data = [line1, line2, line3, line4]
    title = "首次启动耗时"
    create_charts(title, line_data, 6).render()


def test(list1, list2, list3, length):
    line = LineData(list1, "r")
    line2 = LineData(list2, "g")
    line3 = LineData(list3, "b")
    line_data = [line, line2, line3]
    title = "test"
    create_charts(title, line_data, length).render()


if __name__ == '__main__':
    main()
