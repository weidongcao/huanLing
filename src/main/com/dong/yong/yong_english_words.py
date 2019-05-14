"""
把常用英文单词进行五笔编码
"""

import re

fu = 'bcdfghjklmnpqrstvwxyz'
yuan = 'aeiou'

tuple3 = (
    'contr',
    'creat',
    'comp',
    'cons',
    'cont',
    'conv',
    'stat',
    'inst',
    'legi'
    'sens',
    'expe',
    'proc',
    'com',
    'con',
    'the',
    'pro',
    'imp',
    'ser',
    'per',
    'str',
    'div',
    'dve',
    'off',
    'ref',
    'tra',
    'ele',
    'cha',
    'res',
    'sur',
    'whe',
    'pre',
    'sup',
    'sub',
    'pri',
    'gra',
    'dis',
    'des',
    'dec',
    'def',
    'det',
    'app',
    'for',
    'rep',
    'ret',
    'ass',
    'pos',
    'sho',
    'sha',
    'par',
    'adv',
    'acc',
    'att',
    'min',
    'mon',
    'sub',
    'ex',
    'in',
    're',
    'co',
    'un')
# tuple2 = ('ex', 'in', 're', 'co')
combine = ('inter', 'trans', 'there', 'some', 'every', 'part', 'under', 'be', 'life', 'home', 'out', 'down', 'sh')


# tuple2 = ()
# supporter
def get_wubi_key(value):
    if value not in combine:
        i = len(value) - 1
        while i >= 2:
            if value[0:i] in combine:
                key = value[0:2] + value[i:i + 2]
                return key
            i -= 1

    if len(value) >= 4:
        i = len(value) - 1
        while i >= 2:
            if value[0:i] in tuple3:
                key = value[0] + value[i:i + 2] + value[-1:]
                return key
            i -= 1
        # if value.endswith('s'):
        #     key = value[0:2] + value[-2:]
        # elif value.endswith('es'):
        #     key = value[0:2] + value[-3] + value[-1]
        # else:
        #     key = value[0:3] + value[-1]
        key = value[0:3] + value[-1]
    else:
        return value

    return key


def test_key(word_list):
    for i in range(word_list.__len__()):
        print("单词:{} 五笔编码: {}".format(word_list[i], get_wubi_key(word_list[i])))


def add_dict(dt, value):
    key = get_wubi_key(value)

    if key in dt:
        dt[key].append(value)
    else:
        dt[key] = [value]

    return dt


def dict_to_wubi_code(dt, fps):
    content = ''
    for key, value in dt.items():
        content += key + ' ' + ' '.join(value) + '\n'

    with open(fps, 'w') as file:
        file.write(content)


def main():
    with open("words_6000.txt", 'r') as file:
        lines = file.readlines()
    words = []
    word_rank = {}
    repeat = 0
    for i in range(lines.__len__()):
        word = lines[i].strip()
        if words.__contains__(word):
            print("重复的单词:{}".format(word))
            repeat += 1
        else:
            words.append(word)
            word_rank[word] = i + 1
    print("文本文件中重复的单词有 {} 个".format(repeat))
    print("文本文件中单词一共有 {} 个".format(words.__len__()))

    mb4 = {}
    mb3 = {}
    mb2 = {}
    cnt = {'wd5': 0, 'wd4': 0, 'wd3': 0, 'wd2': 0}
    for word in words:
        word = word.lower()
        if len(word) > 4:
            cnt['wd5'] += 1
            mb4 = add_dict(mb4, word)

        elif len(word) == 4:
            cnt['wd4'] += 1
            mb4 = add_dict(mb4, word)
        elif len(word) == 3:
            cnt['wd3'] += 1
            mb3 = add_dict(mb3, word)
        else:
            cnt['wd2'] += 1
            mb2 = add_dict(mb2, word)

    print("3个字母以上有单词有: {}个".format(cnt['wd5'] + cnt['wd4']))
    print("5个字母以上有单词有: {}个, 转换后五笔编码的个数:{}".format(cnt['wd5'], len(mb4)))
    print("4个字母以上有单词有: {}个, 转换后五笔编码的个数:{}".format(cnt['wd4'], cnt['wd4']))
    print("3个字母以上有单词有: {}个, 转换后五笔编码的个数:{}".format(cnt['wd3'], len(mb3)))
    print("2个字母以上有单词有: {}个, 转换后五笔编码的个数:{}".format(cnt['wd2'], len(mb2)))

    cl1 = {}
    cl2 = {}
    cl3 = {}
    cll = {}
    for key, value in mb4.items():
        if value.__len__() == 1:
            cl1[key] = value
        elif value.__len__() == 2:
            cl2[key] = value
        elif value.__len__() == 3:
            cl3[key] = value
        elif value.__len__() >= 4:
            cll[key] = value

    print("没有重码的有: {} 个".format(cl1.__len__()))
    print("重码的有: {} 个".format(mb4.__len__() - cl1.__len__()))

    print("重码率为2有的: {} 个".format(cl2.__len__()))
    print("重码率为3有的: {} 个".format(cl3.__len__()))
    print("重码率为4有的: {} 个".format(cll.__len__()))

    # dict_to_wubi_code(cl1, 'english_word_repeat_1.txt')
    # dict_to_wubi_code(cl2, 'english_word_repeat_2.txt')
    # dict_to_wubi_code(cl3, 'english_word_repeat_3.txt')
    # dict_to_wubi_code(cll, 'english_word_repeat_9.txt')
    i3 = 1
    for key, value in cl2.items():
        print("index = {} --> key = {}, words = {}".format(i3, key, value))
        i3 += 1
    i3 = 1
    for key, value in cl3.items():
        print("index = {} --> key = {}, words = {}".format(i3, key, value))
        i3 += 1
    i3 = 1
    for key, value in cll.items():
        print("index = {} --> key = {}, words = {}".format(i3, key, value))
        i3 += 1


if __name__ == '__main__':
    main()
    test_key(
        ['transmit', 'complain', 'completion', 'comparison', 'complication', 'composition', 'compulsion', 'companion',
         'champion'])
    print(get_wubi_key('supporter'))
    print('presentation'[4:])
