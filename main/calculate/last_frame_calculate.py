# coding=utf-8
import base_utils
from rgb import compare_rgb
from rgb import calculate_repos_rgb
from template_match import match_img
from color_histogram import calculate_by_hists
from clip import clip_specific_pic


last_frame_feature = "./feature/vivoX7_homepage_feature.jpg"
threshold = 0.95  # 准确率测试
base_path = "./extract_folder_all/"
demo_path = "./homepage/"


def last_frame_find_rgb(length, from_index, real_path, real_feature_path, rgb_folder):
    for i in range(from_index, length+1):
        src_file_path = real_path + base_utils.adapter_num(i) + ".jpg"
        feature_name = base_utils.adapter_num(i) + "_feature.jpg"
        match_img(src_file_path, real_feature_path, threshold, real_path + feature_name)
        if base_utils.os.path.exists(real_path + feature_name):
            # 如果识别到了，拿来图片和图库对比，如果当前图片rgb值远大于图库的平均rgb
            # 认为这一帧还在加载中；反之，则认为当前为加载完成帧

            degree = calculate_by_hists(last_frame_feature, real_path + feature_name)
            # 这个值是否还可以再调一下？
            if degree < 0.6:
                continue

            # 识别到才裁剪
            clip_specific_pic(src_file_path)
            if compare_rgb(src_file_path, rgb_folder):
                return i
        print src_file_path + " is not last frame"
    return -1


if __name__ == '__main__':
    print 1
