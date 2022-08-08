# -*- coding: utf-8 -*-
# @Time    : 2020-08-15 19:07
# @Author  : CaoWeidong
# @Email   : caowd1990@163.com
# @File    : compass_dir.py
# @Software: IntelliJ IDEA


"""
将小米摄像头生成的历史视频重构目录，8个小时一个文件夹，并进行压缩，为上传到百度云做准备
"""
import sys
import os
import zipfile
import shutil
from logger import logger

sys.path.append("logger")

title = "摄像头视频-中牟老家后院-"


def get_zip_file(input_path, result):
    files = os.listdir(input_path)
    for file in files:
        if os.path.isdir(input_path + os.path.sep + file):
            get_zip_file(input_path + os.path.sep + file, result)
        else:
            result.append(input_path + os.path.sep + file)


def zip_file_path(input_path, output_path, output_name):
    zip = zipfile.ZipFile(output_path + os.path.sep + output_name, 'w', zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(input_path):
        fpath = path.replace(input_path, '')
        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))

    zip.close()


def main(file_path):
    logger.info("test")

    root_path = os.path.abspath(os.path.dirname(file_path) + os.path.sep + ".")
    dir_list = os.listdir(file_path)

    for index in range(len(dir_list) - 1, -1, -1):
        dir_name = dir_list.pop(index)
        if dir_name.isdigit() and os.path.isdir(dir_name):
            d = dir_name[:8]
            hour = dir_name[-2:]
            new_dir_name = title + d + "-" + str(int(hour) // 8 + 1)
            new_dir_path = root_path + os.path.sep + new_dir_name
            if not os.path.exists(new_dir_path):
                os.mkdir(new_dir_path)

            shutil.move(file_path + os.path.sep + dir_name, new_dir_path)
    logger.info("文件目录重构完成")
    new_dir_list = os.listdir(root_path)
    for i in range(new_dir_list.__len__() - 1, -1, -1):
        dir_name = new_dir_list.pop(i)
        if dir_name.startswith(title):
            if not os.path.exists(root_path + os.path.sep + dir_name + ".zip"):
                logger.info("为文件夹 -> {} 创建压缩文件".format(dir_name))
                zip_file_path(root_path + os.path.sep + dir_name, root_path, dir_name + ".zip")
                logger.info("压缩文件 {} 创建完成".format(dir_name + ".zip"))
            else:
                logger.info("压缩文件: {}已经创建，跳过".format(dir_name + ".zip"))


if __name__ == '__main__':
    main("F:\\摄像头\\摄像头视频-中牟老家后院\\2019MIJIA_RECORD_VIDEO")
    # main("F:\\摄像头\\test\\aaa")
