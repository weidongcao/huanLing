# -*- coding:utf-8 -*-
from pprint import pprint

import xlrd

map = {
    '填表人': 'chat_name',
    '游戏昵称': 'nickname',
    '战力': 'strength',
    'VIP等级': 'vip',
    '步兵数量': 'infantry',
    '骑兵数量': 'cavalry',
    '弓兵数量': 'archers',
    '觉醒武将': 'officer',
    '步兵橙装': 'inf_outfit',
    '步兵橙装专属': 'inf_outfit_pro',
    '骑兵橙装': 'cav_outfit',
    '骑兵橙装专属': 'cav_outfit_pro',
    '弓兵橙装': 'arc_outfit',
    '弓兵橙装专属': 'arc_outfit_pro',
    '联盟': 'union',
    '比赛日期': 'fight_time',
}


def main():
    excel = parse_excel(r'/warehouse/link/Documents/aaa.xlsx')

    header = excel[0]
    idxs = {}
    for i in range(len(header)):
        ch = header[i]
        if ch in map.keys():
            idxs[map[ch]] = i

    dt = []
    for i in range(1, len(excel)):
        line = excel[i]
        bean = {}
        for k, v in idxs.items():
            bean[k] = line[v]

        print(bean)

    pass


def parse_excel(path):
    excel = xlrd.open_workbook(path)
    sheet = excel.sheets()[0]

    lt = []
    for rown in range(sheet.nrows):
        arr = []
        for n in range(sheet.ncols):
            v = sheet.cell_value(rown, n)
            arr.append(v)

        lt.append(arr)

    return lt



if __name__ == '__main__':
    main()
