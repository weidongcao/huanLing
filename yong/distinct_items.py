# -*- coding:utf-8 -*-
import email.policy
import os
from datetime import datetime
from pathlib import Path
import platform

gb18030 = 'gb18030'
# 五笔个人码表根路径
root_dir = None
if platform.system() == 'Windows':
    root_dir = r'D:\Workspace\Github\myconf\yong'
elif platform.system() == 'Linux':
    root_dir = r'/opt/workspace/github/myconf/yong'


def distinct_items(mb_name):
    fpath = Path(root_dir, mb_name)
    with open(fpath, 'r', encoding=gb18030) as file:
        lines = file.read()

    lines = lines.strip()
    lines = lines.split("\n")

    lines = [e.strip() for e in lines]

    distinct_list = []
    for line in lines:
        if line not in distinct_list:
            distinct_list.append(line)

    tpath = Path(fpath.parent, f"{fpath.stem}-{datetime.now().strftime('%Y%m%d')}{fpath.suffix}")

    fpath.rename(tpath)
    with open(fpath, 'w', encoding=gb18030) as f:
        f.write('\n'.join(distinct_list))


def append_items(main_file, append_file, exclude_file):
    main_file = Path(main_file)
    append_file = Path(append_file)
    exclude_file = Path(exclude_file)

    with open(main_file, 'r', encoding=gb18030)as f:
        main_lines = f.read()
        main_lines = main_lines.strip()
        main_lines = main_lines.split("\n")
        main_lines = [e.strip() for e in main_lines]

    with open(append_file, 'r', encoding=gb18030)as f:
        append_lines = f.read()
        append_lines = append_lines.strip()
        append_lines = append_lines.split("\n")
        append_lines = [e.strip() for e in append_lines]

    with open(exclude_file, 'r', encoding=gb18030)as f:
        exclude_lines = f.read()
        exclude_lines = exclude_lines.strip()
        exclude_lines = exclude_lines.split("\n")
        exclude_lines = [e.strip() for e in exclude_lines]

    for line in append_lines:
        if line not in main_lines and line not in exclude_lines:
            main_lines.append(line)

    tpath = Path(main_file.parent, f"{main_file.stem}-{datetime.now().strftime('%Y%m%d')}{main_file.suffix}")

    main_file.rename(tpath)

    with open(main_file, 'w', encoding=gb18030) as f:
        f.write("\n".join(main_lines))


if __name__ == '__main__':
    # distinct_items(Path(root_dir, 'mb/my_info.txt'))
    # distinct_items(Path(root_dir, 'mb/my_ch.txt'))

    append_items(Path(root_dir, "mb/my_ch.txt"), Path(root_dir, "mb/my_chinese.txt"), Path(root_dir, "mb/my_info.txt"))


