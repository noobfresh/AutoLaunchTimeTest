from PIL import Image
import os
import base_utils


def clip(path, count):
    for i in range(1, count + 1):
        complete_path = path + base_utils.adapter_num(i) + ".jpg"
        print complete_path
        img = Image.open(complete_path)
        width = img.size[0]
        height = img.size[1]
        img = img.crop(
            (
                0,
                300,
                width,
                height - 200
            )
        )
        # os.remove(path)
        img.save(base_utils.rename_path(path, i))
        # print base_utils.rename_path(path, i)


def clip_specific_pic(path):
    print path
    img = Image.open(path)
    width = img.size[0]
    height = img.size[1]
    img = img.crop(
        (
            0,
            300,
            width,
            height - 200
        )
    )
    img.save(path)


if __name__ == '__main__':
    # for i in range(1, 28):
    #     path = "../homepage/" + base_utils.adapter_num(i) + ".jpg"
    #     img = Image.open(path)
    #     width = img.size[0]
    #     height = img.size[1]
    #     img = img.crop(
    #         (
    #             0,
    #             300,
    #             width,
    #             height - 200
    #         )
    #     )
    #     # os.remove(path)
    #     img.save("../homepage/" + base_utils.adapter_num(i) + ".jpg")
    #     print path
    print 1