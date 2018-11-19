# coding=utf-8
import os


# path 的相关问题，要想办法统一

def count_file(folder):
    length = len(
        [name for name in os.listdir("./" + folder + "/") if os.path.isfile(os.path.join("./" + folder + "/", name))])
    print length
    return length


def adapter_num(count):
    if count < 10:
        count = "0000" + str(count)
    elif count < 100:
        count = "000" + str(count)
    elif count < 1000:
        count = "00" + str(count)
    elif count < 10000:
        count = "0" + str(count)
    else:
        count = str(count)
    return count


# 矬办法，怪我不熟悉PY
def rename_path(path, count):
    path = path + adapter_num(count) + ".jpg"
    return path


def rename(count):
    if count < 10:
        count = "0000" + str(count) + ".jpg"
    elif count < 100:
        count = "000" + str(count) + ".jpg"
    elif count < 1000:
        count = "00" + str(count) + ".jpg"
    elif count < 10000:
        count = "0" + str(count) + ".jpg"
    else:
        count = str(count) + ".jpg"
    return count


def rename_files():
    i = 1
    path = "../homepage"
    for file1 in os.listdir(path):
        if os.path.isfile(os.path.join(path, file1)) == True:
            new_name = rename(i)
            i += 1
            print new_name
            os.rename(os.path.join(path, file1), os.path.join(path, new_name))
            print "ok"


def count_dirs(path):
    num_dirs = 0  # 路径下文件夹数量

    for root, dirs, files in os.walk(path):  # 遍历统计
        for name in dirs:
            num_dirs += 1
            # print os.path.join(root, name)
    return num_dirs


if __name__ == '__main__':
    rename_files()
