"""
合并用户码表到自己的词库
"""
import os
import platform
import re

import com.dong.yong.yong_util as util

# 汉字
han_zi = 'han_zi'
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
mb[han_zi] = dict()
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

# 需要被删除的编码
dlist = []


def get_dict_from_file(file_path):
    """
    根据五笔码表文件生成对应的字典
    五笔码表文件中的一行:
        grbn 不打了 不接了 不看了 不提了
    值以空格分隔,其中第一个为五笔编码,后面的都为对应的字或词

    生成的字典格式为:
    {"key1": ["词1",词2"], "key2":["词3","词4"]}
    :param file_path:
    :param classify: 分类情况
    :return:
    """
    if os.path.isfile(os.path.join(root_dir, file_path)):
        dt = dict()

        # 将码表文件的所有行读出为一个列表
        with open(os.path.join(root_dir, file_path), 'r', encoding=gb18030) as file:
            lines = file.readlines()

        for line in lines:
            # 一行中的所有值以空格分隔
            elist = line.strip().split(' ')
            # 判断key是否存在于字段中,如果存在追加,如果不存在添加
            if elist[0] not in dt:
                dt[elist[0]] = elist[1:]
            else:
                dt[elist[0]].extend(elist[1:])
    return dt


def check_all_str(s):
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

        # 如果下标为-,表示这个编码需要被删除
        if kv[0][1] == '-':
            dlist.append(line)
            continue
        # 下标
        index = int(kv[0][1])
        # key
        key = kv[0][3:]
        # value
        value = kv[1]
        tup = (index, key, value)

        flat = True
        if check_str(value) == 'yong':
            flat = add_item(mb[phrase], tup)
        elif check_str(value) == 'zh':
            flat = add_item(mb[han_zi], tup)
        elif check_str(value) == 'en':
            flat = add_item(mb[words], tup)
        elif check_str(value) == 'maxture':
            flat = add_item(mb[maxture], tup)
        elif check_str(value) == 'special':
            flat = add_item(mb[special], tup)

        # 如果没有写入用户码表,说明需要写入主码表
        if not flat:
            dlist.append(line)


def add_item(mb, tup):
    """
    为码表字段添加一个新的记录
    :param mb: 类型为字典
    :param tup: 类型为三元组,第一个为下标,第二个为key,第三个为value
    :return: 返回是否插入成功
    """
    index = tup[0]
    key = tup[1]
    value = tup[2]

    if key in mb:
        if index >= mb[key].__len__():  # 如果下标大于词库下标说明是需要在主码表操作
            flat = False
        else:
            if mb[key].__contains__(value):  # 如果用码表已经包含则不写入
                mb[key].insert(index, value)
            flat = True
    else:
        if index > 0:  # 如果用户码表没有,但是却有下标,说明是需要调整主码表顺序
            flat = False
        else:
            mb[key] = [value]
            flat = True
    return flat


def print_dict(dt, desc):
    print("-------------------------------------{}----------------------------------".format(desc))
    i3 = 1
    for key, value in dt.items():
        print("index = {} --> key = {}, words = {}".format(i3, key, value))
        i3 += 1


def main():
    # 个人词库转字典
    mb[han_zi]=get_dict_from_file('mb/my_hanzi.txt')
    mb[phrase]=get_dict_from_file('mb/my_phrase.txt')
    mb[words]=get_dict_from_file('mb/my_words.txt')
    mb[special]=get_dict_from_file('mb/my_special.txt')
    mb[maxture]=get_dict_from_file('mb/my_maxture.txt')

    #
    add_user_to_mb('user.txt')
    # add_user_mb('user.txt')

    print_dict(mb[phrase], '英文短语')
    print_dict(mb[words], "英文单词")
    print_dict(mb[special], '特殊字符')
    print_dict(mb[maxture], '中英混输')
    print_dict(mb[han_zi], '汉字')
    print('\n'.join(dlist))

    util.dict_to_wubi_code(mb[han_zi], os.path.join(root_dir, 'mb/my_hanzi.txt'), gb18030)
    util.dict_to_wubi_code(mb[phrase], os.path.join(root_dir, 'mb/my_phrase.txt'), gb18030)
    util.dict_to_wubi_code(mb[words], os.path.join(root_dir, 'mb/my_words.txt'), gb18030)
    util.dict_to_wubi_code(mb[special], os.path.join(root_dir, 'mb/my_special.txt'), gb18030)
    util.dict_to_wubi_code(mb[maxture], os.path.join(root_dir, 'mb/my_maxture.txt'), gb18030)
    with open(os.path.join(root_dir, 'main_mb.txt'), 'a', encoding=gb18030) as file:
        file.write('\n'.join(dlist))
    util.list_to_wubi_code(dlist, os.path.join(root_dir, 'delete_word.txt'), 'gb18030')


if __name__ == '__main__':
    main()
