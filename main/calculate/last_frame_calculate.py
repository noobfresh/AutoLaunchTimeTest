# coding=utf-8
import base_utils
from log.log import MLog
from rgb import compare_rgb
from rgb import calculate_repos_rgb
from template_match import match_img, isLaunchingPage
from color_histogram import calculate_by_hists
from clip import clip_specific_pic, clip_generate_flag

last_frame_feature = "./feature/vivoX7_homepage_feature.jpg"
threshold = 0.94  # 准确率测试
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

            degree = calculate_by_hists(real_feature_path, real_path + feature_name)
            print "degree = {}    -----------------------------".format(degree)
            # 这个值是否还可以再调一下？
            if degree < 0.53:
                continue

            # 识别到才裁剪
            clip_specific_pic(src_file_path)
            if compare_rgb(src_file_path, rgb_folder):
                return i
        MLog.debug("last_frame_find_rgb: " + src_file_path + " is not last frame")
    return -1


def new_last_frame_find_rgb(start_index, length, real_path, real_feature_path, rgb_folder):
    for i in range(start_index, length+1):
        src_file_path = real_path + base_utils.adapter_num(i) + ".jpg"
        feature_name = base_utils.adapter_num(i) + "_feature.jpg"
        match_img(src_file_path, real_feature_path, threshold, real_path + feature_name)
        if base_utils.os.path.exists(real_path + feature_name):
            # 如果识别到了，拿来图片和图库对比，如果当前图片rgb值远大于图库的平均rgb
            # 认为这一帧还在加载中；反之，则认为当前为加载完成帧

            degree = calculate_by_hists(last_frame_feature, real_path + feature_name)
            # 这个值是否还可以再调一下？
            MLog.debug(u"new_last_frame_find_rgb: color degreee = {}".format(str(degree)))
            if degree < 0.41:
                continue

            # 识别到才裁剪
            clip_specific_pic(src_file_path)
            if compare_rgb(src_file_path, rgb_folder):
                return i
        MLog.debug("new_last_frame_find_rgb: " + src_file_path + " is not last frame")
    return -1


# 把启动结束帧和末尾帧的计算整合
def last_and_launching_frame_find_rgb(length, from_index, real_path, real_launching_feature_path,
                                      real_last_feature_path, rgb_folder):
    launching_homepage_flag = True
    launching_index = -1
    homepage_index = -1
    for i in range(from_index+2, length+1):
        src_file_path = real_path + base_utils.adapter_num(i) + ".jpg"
        feature_name = base_utils.adapter_num(i) + "_feature.jpg"

        if launching_homepage_flag:
            # 进入启动页匹配
            flag = isLaunchingPage(src_file_path, real_launching_feature_path)
            if flag:
                MLog.debug("find_lanching_end_frame: " + src_file_path + " is launching frame")
                continue
            else:
                # 没匹配到，则先记录为启动结束帧，记得往前取一帧
                launching_index = i - 1
                clip_generate_flag(real_path + base_utils.adapter_num(i - 1) + ".jpg",
                                   real_path + base_utils.adapter_num(i - 1) + "_feature.jpg")
                MLog.debug("find_lanching_end_frame: " + src_file_path + " is not launching frame!!!!")
                launching_homepage_flag = False
        else:
            match_img(src_file_path, real_last_feature_path, threshold, real_path + feature_name)
            if base_utils.os.path.exists(real_path + feature_name):
                # 如果识别到了，拿来图片和图库对比，如果当前图片rgb值远大于图库的平均rgb
                # 认为这一帧还在加载中；反之，则认为当前为加载完成帧

                degree = calculate_by_hists(real_last_feature_path, real_path + feature_name)
                print "degree = {}    -----------------------------".format(degree)
                # 这个值是否还可以再调一下？这个值太难取了，有些手机的帧很模糊，有些手机又特别清楚
                if degree < 0.65:
                    continue

                # 识别到才裁剪，这个裁剪要改一下，每次都被剪掉，剪爆了，就很尴尬了
                dst_path = real_path + base_utils.adapter_num(i) + "_clip.jpg"
                clip_specific_pic(src_file_path, dst_path)
                if compare_rgb(dst_path, rgb_folder):
                    homepage_index = i
                    return launching_index, homepage_index
            else:
                # 没找到首页特征图时，去找启动页的特征图
                tmp_flag = isLaunchingPage(src_file_path, real_launching_feature_path)
                if tmp_flag:
                    launching_homepage_flag = True
                    MLog.info("we find launching  pic agagin, the index = {}".format(i))
                    continue
        MLog.debug("last_frame_find_rgb: " + src_file_path + " is not last frame")
    return launching_index, homepage_index


# 针对虎牙的首次启动做的适配
def huya_first_find_frame(length, from_index, real_path, real_launching_feature_path,
                          real_last_feature_path, rgb_folder):
    launching_homepage_flag = True
    launching_index = -1
    homepage_index = -1
    for i in range(from_index+2, length+1):
        src_file_path = real_path + base_utils.adapter_num(i) + ".jpg"
        feature_name = base_utils.adapter_num(i) + "_feature.jpg"

        if launching_homepage_flag:
            # 进入启动页匹配
            flag = isLaunchingPage(src_file_path, real_launching_feature_path)
            if flag:
                MLog.debug("find_lanching_end_frame: " + src_file_path + " is launching frame")
                continue
            else:
                # 没匹配到，则先记录为启动结束帧，记得往前取一帧
                launching_index = i - 1
                clip_generate_flag(real_path + base_utils.adapter_num(i - 1) + ".jpg",
                                   real_path + base_utils.adapter_num(i - 1) + "_feature.jpg")
                MLog.debug("find_lanching_end_frame: " + src_file_path + " is not launching frame!!!!")
                launching_homepage_flag = False
        else:
            match_img(src_file_path, real_last_feature_path, threshold, real_path + feature_name)
            if base_utils.os.path.exists(real_path + feature_name):
                # 如果识别到了，拿来图片和图库对比，如果当前图片rgb值远大于图库的平均rgb
                # 认为这一帧还在加载中；反之，则认为当前为加载完成帧

                degree = calculate_by_hists(real_last_feature_path, real_path + feature_name)
                print "degree = {}    -----------------------------".format(degree)
                # 这个值是否还可以再调一下？这个值太难取了，有些手机的帧很模糊，有些手机又特别清楚
                if degree < 0.735:
                    continue

                # 识别到才裁剪
                homepage_index = i
                return launching_index, homepage_index
            else:
                # 没找到首页特征图时，去找启动页的特征图
                tmp_flag = isLaunchingPage(src_file_path, real_launching_feature_path)
                if tmp_flag:
                    launching_homepage_flag = True
                    MLog.info("we find launching  pic agagin, the index = {}".format(i))
                    continue
        MLog.debug("last_frame_find_rgb: " + src_file_path + " is not last frame")
    return launching_index, homepage_index


if __name__ == '__main__':
    print 1
