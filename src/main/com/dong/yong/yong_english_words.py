"""
把常用英文单词转为yong码表
"""

import re


def add_dict(dt, value):
    if len(value) > 4:
        key = value[0:3] + value[-1::]
        # key = value[0:4]
    else:
        key = value

    if key in dt:
        dt[key].append(value)
    else:
        dt[key] = [value]

    return dt

def get_words1():
    pattern = re.compile('^\d+\s+(\w+)\s', re.S)
    words = []
    # with open("/home/wedo/Documents/common_english_words.txt", 'r') as file:
    with open("/home/wedo/Documents/all_english_words.txt", 'r') as file:
        lines = file.readlines()

    print("总行数:{}".format(lines.__len__()))
    for i in range(lines.__len__()):
        line = lines[i]
        ws = re.findall(pattern, line)
        if ws.__len__() == 0:
            print("没有匹配到 --> {}".format(line))
        for word in iter(ws):
            word = word.strip()
            # print("第{}行:{}".format(i, word))
            if word:
                if not words.__contains__(word):
                    words.append(word)
                else:
                    print("重复的单词 --> {}".format(word))
            else:
                print("空的单词 --> {}".format(word))

    # print(words)
    # print("word count --> {}".format(words.__len__()))


def main():
    with open("/home/wedo/Documents/words.txt", 'r') as file:
        lines = file.readlines()
    words = []
    for i in range(lines.__len__()):
        words.append(lines[i].strip())
    mb5 = {}
    mb4 = {}
    mb3 = {}
    mb2 = {}
    for word in words:
        word = word.lower()
        if len(word) > 4:
            mb5 = add_dict(mb5, word)
        elif len(word) == 4:
            mb4 = add_dict(mb4, word)
        elif len(word) == 3:
            mb3 = add_dict(mb3, word)
        else:
            mb2 = add_dict(mb2, word)

    print("{}个单词转为五笔码表的个数:{}".format(len(lines), len(mb5)))
    # for key, value in mb5.items():
    #     print("{} : {}".format(key, value))


if __name__ == '__main__':
    main()