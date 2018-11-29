from calculate import base_utils
from calculate.clip import clip_generate_flag
from calculate.template_match import isLaunchingPage
from log.log import MLog

threshold = 0.95


def find_lanching_end_frame(start_index, length, feature_path, folder_path):
    for i in range(start_index, length+1):
        src_file_path = folder_path + base_utils.adapter_num(i) + ".jpg"
        if isLaunchingPage(src_file_path, feature_path):
            MLog.debug("find_lanching_end_frame: " + src_file_path + " is launching frame")
            continue
        else:
            MLog.debug("find_lanching_end_frame: " + src_file_path + " is not launching frame!!!!")
            clip_generate_flag(folder_path + base_utils.adapter_num(i-1) + ".jpg",
                               folder_path + base_utils.adapter_num(i - 1) + "_feature.jpg")
            return i - 1
    return -1
