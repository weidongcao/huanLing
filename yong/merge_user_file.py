# -*- coding:utf-8 -*-
"""
合并用户码表到自己的词库
"""
import os
import platform
import re

import yong_util as util

# 五笔源库
wbx = 'wbx'
# 汉字
chinese = 'chinese'
# 单词
words = 'words'
# 英文短语
phrase = 'phrase'
# 特殊格式
special = 'special'
# 中英混输
maxture = 'maxture'
# 编码格式:GB18030
gb18030 = 'gb18030'

# mb是五笔个人码表的意思
mb = dict()
mb[chinese] = dict()
mb[words] = dict()
mb[phrase] = dict()
mb[special] = dict()
mb[maxture] = dict()


# 五笔个人码表根路径
root_dir = None
if platform.system() == 'Windows':
    root_dir = r'D:\Workspace\Github\myconf\yong'
elif platform.system() == 'Linux':
    root_dir = r'/opt/workspace/github/myconf/yong'

wbx_title = """name=五笔
key=abcdefghijklmnopqrstuvwxyz
len=4
wildcard=z
dwf=1
auto_clear=4
assist=z mb/pinyin.txt
code_e2=p11+p12+p21+p22
code_e3=p11+p21+p31+p32
code_a4=p11+p21+p31+n11
[DATA]
"""

# 需要被删除的编码
dlist = []


def get_dict_from_file(mb_name):
    """
    根据五笔码表文件生成对应的字典
    五笔码表文件中的一行:
        grbn 不打了 不接了 不看了 不提了
    值以空格分隔,其中第一个为五笔编码,后面的都为对应的字或词

    生成的字典格式为:
    {"key1": ["词1",词2"], "key2":["词3","词4"]}
    :param mb_name:
    :param classify: 分类情况
    :return:
    """
    if os.path.isfile(os.path.join(root_dir, mb_name)):
        dt = dict()

        # 将码表文件的所有行读出为一个列表
        with open(os.path.join(root_dir, mb_name), 'r', encoding=gb18030) as file:
            lines = file.readlines()
        line_number = 0
        if mb_name.endswith("wbx.txt"):
            line_number = 11

        for index in range(line_number, len(lines)):
            line = lines[index].strip()
            if not line:
                continue
            # 一行中的所有值以空格分隔
            elist = line.split(' ')

            # 去重
            l = []
            for e in elist[1:]:
                if e not in l:
                    l.append(e)
            # 判断key是否存在于字段中,如果存在追加,如果不存在添加
            if elist[0] not in dt:
                dt[elist[0]] = l
            else:
                dt[elist[0]].extend(l)
        return dt
    return None


def check_all_str(s):
    """
    检查是否字母数字下划线
    :param s:
    :return:
    """
    alpha = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-'
    for c in s:
        if c not in alpha:
            return False

    return True


def check_str(s):
    """
    判断字符串是否包含中文
    :param check_str:
    :return:
    """

    result = ''
    s.encode('utf-8')
    if '\u4e00' <= s <= '\u9fa5':  # 全部为汉字
        result = "zh"
    elif s.__contains__('$_'):  # 小小输入法
        result = 'yong'
    elif s.isdigit():  # 全部为数字
        result = 'number'
    elif check_all_str(s):  # 字母
        result = "en"
    else:
        if s.isalnum():
            for c in s:
                if '\u4e00' <= c <= '\u9fa5':  # 包含汉字
                    result = 'maxture'
        else:
            result = 'special'
    return result


def add_user_to_mb(file_path):
    """
    user.txt词库转字典并添加到个人码表(mb)字典中
    user.txt词库一条数据的格式为:
        {0}ctxy 双系统
    {}里的为下标,中间的为五笔编码,空格后面的为词
    :param file_path:
    :return:
    """
    with open(os.path.join(root_dir, file_path), 'r', encoding='gb18030') as file:
        lines = file.readlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        kv = line.strip().split(' ')

        # 下标
        index = kv[0][1]
        # key
        key = kv[0][3:]
        # value
        value = kv[1]
        tup = (index, key, value)

        if index == '-':
            # 如果下标为-,表示这个编码需要被删除
            dlist.append(line)
            del_item(mb, tup)
        else:
            # 如果下标不为-,表示这个编码为新增或者调换顺序
            if check_str(value) == 'yong':
                flat = add_item(mb[phrase], tup)
            elif check_str(value) == 'zh':
                flat = add_item(mb[chinese], tup)
            elif check_str(value) == 'en':
                flat = add_item(mb[words], tup)
            elif check_str(value) == 'maxture':
                flat = add_item(mb[maxture], tup)
            elif check_str(value) == 'special':
                flat = add_item(mb[special], tup)


def add_item(mb, tup):
    """
    为码表字段添加一个新的记录
    :param mb: 类型为字典
    :param tup: 类型为三元组,第一个为下标,第二个为key,第三个为value
    :return: 返回是否插入成功
    """
    index = int(tup[0])
    key = tup[1]
    value = tup[2]

    if key in mb:
        if index >= mb[key].__len__():  # 如果下标大于词库下标说明是需要在主码表操作
            flat = False
        else:
            if not mb[key].__contains__(value):  # 如果用码表已经包含则不写入
                mb[key].insert(index, value)
            flat = True
    else:
        if index > 0:  # 如果用户码表没有,但是却有下标,说明是需要调整主码表顺序
            flat = False
        else:
            mb[key] = [value]
            flat = True
    return flat


def del_item(mb, tup):
    """
    删除一条记录
    :param mb:
    :param tup:
    :return:
    """
    key = tup[1]
    value = tup[2]

    for (mb_name, dt) in mb.items():
        if key in dt.keys():
            if value in dt[key]:
                dt[key].remove(value)
                print("删除记录成功, 词库: {}, {} --> {}".format(mb_name, key, value))
                break


def print_dict(dt, desc):
    print("-------------------------------------{}----------------------------------".format(desc))
    i3 = 1
    for key, value in dt.items():
        print("index = {} --> key = {}, words = {}".format(i3, key, value))
        i3 += 1


def main():
    # 个人词库转字典
    # 主码表
    mb[wbx]=get_dict_from_file('mb/wbx.txt')
    # 汉字
    mb[chinese]=get_dict_from_file('mb/my_chinese.txt')
    # 词组
    mb[phrase]=get_dict_from_file('mb/my_phrase.txt')
    # 英语
    mb[words]=get_dict_from_file('mb/my_words.txt')
    # 特殊字符
    mb[special]=get_dict_from_file('mb/my_special.txt')
    #混合字符
    mb[maxture]=get_dict_from_file('mb/my_maxture.txt')

    #
    add_user_to_mb('user.txt')
    # add_user_mb('user.txt')

    # print_dict(mb[phrase], '英文短语')
    # print_dict(mb[words], "英文单词")
    # print_dict(mb[special], '特殊字符')
    # print_dict(mb[maxture], '中英混输')
    # print_dict(mb[chinese], '汉字')
    # print('\n'.join(dlist))

    # 将汉字写入个人词库
    util.dict_to_wubi_code(mb[chinese], os.path.join(root_dir, 'mb/my_chinese.txt'), gb18030)
    # 将英文短语写入个人词库
    util.dict_to_wubi_code(mb[phrase], os.path.join(root_dir, 'mb/my_phrase.txt'), gb18030)
    # 将英文单词写入个人词库
    util.dict_to_wubi_code(mb[words], os.path.join(root_dir, 'mb/my_words.txt'), gb18030)
    # 将特殊字符写入个人词库
    util.dict_to_wubi_code(mb[special], os.path.join(root_dir, 'mb/my_special.txt'), gb18030)
    # 将中英混输写入个人词库
    util.dict_to_wubi_code(mb[maxture], os.path.join(root_dir, 'mb/my_maxture.txt'), gb18030)

    # 写入之后原来的user.txt保持不变,确认后请手动删除

    clist = []
    for key, value in mb[wbx].items():
        clist.append(key + ' ' + ' '.join(value))
    clist.sort()
    with open(os.path.join(root_dir, 'mb/wbx.txt'), 'w', encoding=gb18030) as file:
        file.write(wbx_title)
        file.write('\n'.join(clist))

    util.list_to_wubi_code(dlist, os.path.join(root_dir, 'delete_word.txt'), 'gb18030')


if __name__ == '__main__':
    main()
