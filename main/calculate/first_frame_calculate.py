# coding=utf-8
import base_utils
from template_match import match_img
from color_histogram import calculate_by_hists

first_frame_feature = "./feature/vivoX7_launch_feature.jpg"  # 配置项
threshold = 0.95
base_path = "./extract_folder_all/"


# 首帧计算过程
def first_frame_find(length, real_path, real_feature_path):
    for i in range(1, length+1):
        src_file_path = real_path + base_utils.adapter_num(i) + ".jpg"
        feature_name = real_path + base_utils.adapter_num(i) + "_feature.jpg"
        # print src_file_path
        # print real_feature_path
        match_img(src_file_path, real_feature_path, threshold, feature_name)
        if base_utils.os.path.exists(feature_name):
            # 首帧思路，如果识别到了，取出截取部分与特征图做个彩色直方图对比，确定
            degree = calculate_by_hists(real_feature_path, feature_name)
            # print degree
            if degree > 0.6:
                return i
        print src_file_path + " is not first frame"
    return -1


def new_first_frame_find(start_index, length, real_path, real_feature_path):
    for i in range(start_index, length+1):
        src_file_path = real_path + base_utils.adapter_num(i) + ".jpg"
        feature_name = real_path + base_utils.adapter_num(i) + "_feature.jpg"
        # print src_file_path
        # print real_feature_path
        match_img(src_file_path, real_feature_path, threshold, feature_name)
        if base_utils.os.path.exists(feature_name):
            # 首帧思路，如果识别到了，取出截取部分与特征图做个彩色直方图对比，确定
            degree = calculate_by_hists(real_feature_path, feature_name)
            # print degree
            if degree > 0.6:
                return i
        print src_file_path + " is not first frame"
    return -1


if __name__ == '__main__':
    index = first_frame_find()
    if index > 0:
        print "the first frame index = {}".format(index)
    else:
        print "i have not found first frame"
