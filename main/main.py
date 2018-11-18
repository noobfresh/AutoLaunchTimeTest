# coding=utf-8
from calculate.first_frame_calculate import first_frame_find
from calculate.last_frame_calculate import last_frame_find_rgb
from calculate.base_utils import count_file
from calculate.base_utils import count_dirs
from calculate.clip import clip
from screen_record import start_python
from screen_record import getDeviceInfo
import re
import json

if __name__ == '__main__':
    # start_python()

    # 生成好照片
    device_name = getDeviceInfo()
    device_name = re.sub('\s', '', device_name)
    # print device_name
    dir_count = count_dirs("./" + device_name)
    obj = {"app": "7.12", "phone": device_name}
    mean_time = 0
    # for i in range(0, dir_count):
    #     # 取指定目录下的file count
    #     file_count = count_file(device_name + "/" + device_name + "_" + str(i))
    #     real_path = "./" + device_name + "/" + device_name + "_" + str(i) + "/"
    #     # 优化点，没有必要全裁一遍其实
    #     clip(real_path, file_count)
    #     real_first_feature_path = "./feature/" + device_name + "_launch_feature.jpg"
    #     first = first_frame_find(file_count, real_path, real_first_feature_path)
    #     # # 中间会生成多余的照片影响
    #     real_last_feature_path = "./feature/" + device_name + "_homepage_feature.jpg"
    #     last = last_frame_find_rgb(file_count, first)
    #     time = (last - first + 1) * (1000 / 60)
    #     mean_time += time
    # mean_time /= dir_count
    obj["first_start"] = str(4978)
    obj["start"] = ""
    json_data = [obj]
    print json.dumps(json_data)

