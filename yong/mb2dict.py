# -*- coding:utf-8 -*-
'''
五笔码表转字典
'''


def get_dict_from_mb(fps, dt):
    with open(fps, 'r') as file:
        lines = file.readlines()
    for line in lines.__iter__():
        kv = line.strip().split(' ')
        if kv:
            if kv[0] in dt:
                dt[kv[0]].extend(kv[1:])
            else:
                dt[kv[0]] = kv[1:]
    return dt


def main():
    dt = {}
    dt = get_dict_from_mb('english_word_repeat_1.txt', dt)
    dt = get_dict_from_mb('english_word_repeat_2.txt', dt)
    dt = get_dict_from_mb('english_word_repeat_3.txt', dt)
    dt = get_dict_from_mb('english_word_repeat_9.txt', dt)

    cl1 = {}
    cl2 = {}
    cl3 = {}
    cll = {}
    for key, value in dt.items():
        if value.__len__() == 1:
            cl1[key] = value
        elif value.__len__() == 2:
            cl2[key] = value
        elif value.__len__() == 3:
            cl3[key] = value
        elif value.__len__() >= 4:
            cll[key] = value

    print("没有重码的有: {} 个".format(cl1.__len__()))
    print("重码的有: {} 个".format(dt.__len__() - cl1.__len__()))

    print("重码率为2有的: {} 个".format(cl2.__len__()))
    print("重码率为3有的: {} 个".format(cl3.__len__()))
    print("重码率为4有的: {} 个".format(cll.__len__()))

    content = ''
    for key, value in dt.items():
        content += key + ' ' + ' '.join(value) + '\n'

    # with open('words.txt', 'w') as file:
    #     file.write(content)

    # i3 = 1
    # for key, value in cl2.items():
    #     print("index = {} --> key = {}, words = {}".format(i3, key, value))
    #     i3 += 1
    # i3 = 1
    # for key, value in cl3.items():
    #     print("index = {} --> key = {}, words = {}".format(i3, key, value))
    #     i3 += 1
    i3 = 1
    for key, value in cll.items():
        print("index = {} --> key = {}, words = {}".format(i3, key, value))
        i3 += 1


if __name__ == '__main__':
    with open('words_6000.txt', 'r') as file:
        lines = file.readlines()

    words = []
    for i in range(lines.__len__()):
        word = lines[i].strip().lower()
        words.append(word)
    words.sort()
    # print(" ".join(words))
    with open('words.txt', 'w') as file:
        file.write("\n".join(words))

