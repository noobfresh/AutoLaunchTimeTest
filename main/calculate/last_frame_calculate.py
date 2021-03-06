# coding=utf-8
import base_utils
from calculate.other_algorithm import phashfinal
from log.log import MLog
from rgb import compare_rgb, calcule_specific_area_rgb, is_ent_black_point, is_in_portrait_live_room, \
    is_ent_all_black_point, is_in_loading
from PIL import Image
from rgb import calculate_repos_rgb
from template_match import match_img, isLaunchingPage, isHomepageFinish, isHomePageLoadFinish
from color_histogram import calculate_by_hists
from clip import clip_specific_pic, clip_generate_flag, clip_half_pic

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
            # 首页匹配
            # 取巧操作，取右下角的点，看他是不是纯白，来过滤掉还有蒙层的帧
            if not isHomepageFinish(src_file_path):
                MLog.info("index = {} is not at homepage".format(i))
                continue
            match_img(src_file_path, real_last_feature_path, threshold, real_path + feature_name)
            if base_utils.os.path.exists(real_path + feature_name):
                # 如果识别到了，拿来图片和图库对比，如果当前图片rgb值远大于图库的平均rgb
                # 认为这一帧还在加载中；反之，则认为当前为加载完成帧

                degree = calculate_by_hists(real_last_feature_path, real_path + feature_name)
                print "degree = {}    -----------------------------".format(degree)
                # 这个值是否还可以再调一下？这个值太难取了，有些手机的帧很模糊，有些手机又特别清楚
                if degree < 0.65:
                    continue

                dst_path = real_path + base_utils.adapter_num(i) + "_clip.jpg"
                clip_specific_pic(src_file_path, dst_path)
                if compare_rgb(dst_path, rgb_folder):
                    MLog.debug("the rgb test is passed")
                    if isHomePageLoadFinish(src_file_path, src_file_path[0: len(src_file_path) - 4] + "_loaded.jpg"):
                        MLog.debug("the loading test is passed")
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


def enter_ent_last_frame_find(start_index, file_count, path, feature_path):
    dp = base_utils.get_dp()  # 这两个是常用的，应该预先取
    img = Image.open(path + "00001.jpg")
    width = img.size[0]  # 这两个是常用的，应该预先取
    current_rate = 1.0
    enter_live_room_index = -1
    last_index = -1
    for i in range(start_index, file_count):
        src_file_path = path + base_utils.adapter_num(i) + ".jpg"
        # 阈值先设置为0.9，暂时不知道用截图裁剪出来的图片，去找图，会发生什么事
        match_img(src_file_path, feature_path, 0.8, path + base_utils.adapter_num(i) + "_feature.jpg")
        # 如果裁剪到图片的话，就证明还没进入到直播间
        if base_utils.os.path.exists(path + base_utils.adapter_num(i) + "_feature.jpg"):
            print "i find the feature pic! and current rate = {}".format(current_rate)
            continue
        else:
            # 如果，发现当前特征图，无法在当前图片匹配到时，对原有特征图进行对半裁剪，然后再对原有图片进行匹配，若匹配到，跳出循环继续下一张找图
            # 若无匹配到，则重复上述过程，直至特征图被裁剪到最一开始的 1/8时，若还未找到，则认为已经进入直播间
            # flag = False
            # while current_rate > 0.125:
            #     current_rate /= 2
            #     clip_half_pic(feature_path)
            #     print "i have cut a half the feature pic. current rate = {}".format(current_rate)
            #     match_img(src_file_path, feature_path, 0.9, path + base_utils.adapter_num(i) + "_feature.jpg")
            #     if base_utils.os.path.exists(path + base_utils.adapter_num(i) + "_feature.jpg"):
            #         print "i find the feature pic! and current rate = {}".format(current_rate)
            #         flag = True
            # if flag:
            #     continue
            # 认为进入了直播间
            print "i think it is entering liveroom index = {}, current dp = {}".format(i, dp)
            enter_live_room_index = i
            break
    if enter_live_room_index == -1:
        return
    for i in range(enter_live_room_index, file_count):
        src_file_path = path + base_utils.adapter_num(i) + ".jpg"
        top_margin = 80 * dp
        # 不取0.75这么多
        clip_video_height = width * 0.5
        # 然后再计算，认为的视频区域，把他的平均RGB算出来，和平时没视频时的RGB值做比较
        print "index = " + str(i)
        r, g, b = calcule_specific_area_rgb(src_file_path, width*0.75, top_margin, width,
                                        top_margin + clip_video_height)
        # 如果直播间直播内容比较暗的话，这个判断就会有问题
        if r >= 80 and g >= 80 and b >= 80:
            last_index = i
            print "i think the last frame index is {}".format(last_index)
            break
    if last_index == -1:
        print "i have not found the last frame"
    return enter_live_room_index, last_index


# 专门为了淡入效果做的算法适配（YY）
def enter_ent_last_frame_find_fade_in(start_index, file_count, basepath):
    last_index = -1
    for i in range(start_index, file_count):
        src_file_path1 = basepath + base_utils.adapter_num(i) + ".jpg"
        src_file_path2 = basepath + base_utils.adapter_num(i+1) + ".jpg"
        compareValue = phashfinal(src_file_path1, src_file_path2)
        print "No.{} and No.{} compare, value = {}".format(i, i+1, compareValue)
        if compareValue < 0.80:
            # 变化率很大，则再判断下是否正在直播间内（右下角的RGB值），经测试证明，这种判断方法只针对横屏开播有效，竖屏开播就GG了
            if is_ent_black_point(src_file_path2):
                last_index = i+1
                break
    if last_index == -1:
        print "i have not found the last frame"
    return 0, last_index


def enter_ent_last_frame_find_fade_in_test(start_index, file_count, basepath):
    last_index = -1
    skip_compare = False
    in_portrait = False
    i = start_index
    while i < file_count:
        src_file_path1 = basepath + base_utils.adapter_num(i) + ".jpg"
        src_file_path2 = basepath + base_utils.adapter_num(i+1) + ".jpg"
        compareValue = phashfinal(src_file_path1, src_file_path2)
        print "No.{} and No.{} compare, value = {}".format(i, i+1, compareValue)
        if compareValue < 0.80 or skip_compare:

            # 变化率很大，则再判断下是否正在直播间内（右下角的RGB值），经测试证明，这种判断方法只针对横屏开播有效，竖屏开播就GG了
            if is_ent_black_point(src_file_path2):
                print "find landscape last index"
                last_index = i+1
                break

            # 还得顺便是不是竖屏开播，这个怎么判断呢
            # 思路无可奈何之下改变为，如果发现有全黑屏的情况的话，就认为进入了竖屏判断条件
            # 然后跳过5张图
            if is_ent_all_black_point(src_file_path2):
                print "it is in portrait"
                in_portrait = True
                skip_compare = True
                i = i + 5
                continue

            # 捕获竖屏开播情况， 左上左下，右上右下都是有颜色的，就算捕获？
            if in_portrait and not is_in_loading(src_file_path2) and is_in_portrait_live_room(src_file_path2):
                print "found portrait last index"
                last_index = i+1
                break

            skip_compare = False
        i += 1
    if last_index == -1:
        print "i have not found the last frame"
    return 0, last_index


if __name__ == '__main__':
    # print enter_ent_last_frame_find(135, 160, "../screenrecord/MI8_enterliveroom/MI8_enterliveroom_0/",
    #                           "F:\\cvtest\\feature.jpg")
    print enter_ent_last_frame_find_fade_in_test(131, 300,
                                                 "F:\github\main\screenrecord\special\MiNote2_enterliveroom_3\\")
    print 1
