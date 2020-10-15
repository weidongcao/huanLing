import json
import re
import time

import requests
import datetime
import pymysql
from requests.adapters import HTTPAdapter

from logger import logger

from elasticsearch import Elasticsearch
from elasticsearch import helpers
from dao.MysqlHelper import MysqlHelper

# 爬虫获取页面数据
url = "https://flash-api.jin10.com/get_flash_list"
header = {
    "x-app-id": "SO1EJGmNgCtmpcPF",
    "x-version": "1.0.0",
}
queryParam = {
    "max_time": "2020-09-03 22:00:00",
    "channel": "-8200",
}

with open("info.json", 'r') as f:
    aaa = json.load(f)
class_dict = dict()
mc = aaa["mapping_class"]
for c1 in mc.keys():
    if mc[c1]:
        for c2 in mc[c1].keys():
            if c2 == "flags":
                for e in mc[c1][c2]:
                    class_dict[e] = (c1, None)
            elif mc[c1][c2]:
                for c3 in mc[c1][c2]:
                    class_dict[c3] = (c1, c2)

            else:
                class_dict[c2] = (c1, c2)
    else:
        class_dict[c1] = (c1, None)
country_dict = dict()
for e in aaa["country"]:
    country_dict[e] = e
for c in aaa["mapping_country"].keys():
    for e in aaa["mapping_country"][c]:
        if e:
            country_dict[e] = c
for c in aaa["mapping_company"].keys():
    for e in aaa["mapping_company"][c]:
        if e:
            country_dict[e] = c
for c in aaa["mapping_distinct"].keys():
    for e in aaa["mapping_distinct"][c]:
        if e:
            country_dict[e] = c

insert_template = "insert into jin10(jid, createTime, country, class_1, class_2, speaker, info, outline, provenance) values (%s, %s, %s, %s, %s, %s, %s, %s, %s) on duplicate key update country=values(country)"

mysql_helper = MysqlHelper("wedo.com", "wedo", "sdfsdf", "wedo")

restart = True
if restart:
    record_dict = {}
else:
    record_dict = json.load(open('record.json', 'r'))
if not record_dict.__contains__("min_time"):
    record_dict["min_time"] = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")
if not record_dict.__contains__("max_time"):
    record_dict["max_time"] = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S")


def clean_str(s):
    if not s:
        return None
    else:
        s = s.strip()
        p = re.compile("<span(.*?)</span>")
        s = p.sub('', s)
        s = s.strip()
        s = s.replace("<b>", "").replace("</b>", "")
        s = s.replace("<br/>", "")
        return s


def mapping_tag(content, dt):
    if content:
        for k in dt.keys():
            for e in dt[k]:
                if e and content.__contains__(e):
                    return e, k
    return None


def parse_flag(content):
    class_1 = None
    class_2 = None
    country = None
    flist = []
    clist = []
    original_flag = None
    for t in class_dict.keys():
        if content.__contains__(t):
            flist.append((t, class_dict[t]))

    if len(flist) == 1:
        class_1 = flist[0][1][0]
        class_2 = flist[0][1][1]
        original_flag = flist[0][0]
    elif len(flist) > 1:
        i = 100000
        for e in flist:
            ind = content.index(e[0])
            if 0 <= ind < i:
                i = ind
                class_1 = e[1][0]
                class_2 = e[1][1]
                original_flag = e[0]

    for c in country_dict.keys():
        if content.__contains__(c):
            clist.append((c, country_dict[c]))
    if class_2 and country_dict.__contains__(class_2):
        clist.append((original_flag, country_dict[class_2]))

    a = mapping_tag(content, aaa["mapping_company"])
    if a and not class_1:
        if a[1] == "中国":
            class_1 = "A股"
        elif a[1] == "美国":
            class_1 = "美股"
        else:
            class_1 = "股票"
        clist.append(a)

    clist = list(filter(None, clist))
    if len(clist) == 1:
        country = clist[0][1]
    elif len(clist):
        i = 10000
        for e in clist:
            ind = content.index(e[0])
            if 0 <= ind < i:
                i = ind
                country = e[1]
    if class_2 == class_1:
        class_2 = None
    return country, class_1, class_2


def parse_content(content):
    content = clean_str(content)
    country = None
    class_1 = None
    class_2 = None
    outline = None
    speaker = None
    provenance = None
    info = None

    if content:
        country, class_1, class_2 = parse_flag(content)
        if content.startswith("【"):
            content = content.replace("【", "")
            if content.__contains__("："):
                speaker = content.split("：", 1)[0]
                outline = content.split("：", 1)[1]
                info = content.split("】")[1]

            else:
                if content.__contains__("】"):
                    speaker = content.split("】")[0]
                    info = content.split("】")[1]
                else:
                    info = content

        elif content.__contains__("："):
            speaker = content.split("：", 1)[0]
            info = content.split("：", 1)[1]
        else:
            info = content

        if content.endswith("）"):
            p = "（"
            if not info.__contains__(p):
                p = "("
            arr = info.rsplit(p, 1)
            info = arr[0]
            if len(arr) > 1:
                provenance = arr[1]
                provenance = provenance.replace("）", "")

    return country, class_1, class_2, speaker, info, outline, provenance


def convert_es_data(d):
    # jid, createTime, country, class_1, class_2, speaker, info, outline, provenance
    # 转UTC时间
    t = datetime.datetime.strptime(d[1], "%Y-%m-%d %H:%M:%S")
    t += datetime.timedelta(hours=-8)
    ts = datetime.datetime.strftime(t, "%Y-%m-%d %H:%M:%S")

    doc = {"createTime": ts, "info": d[6]}
    if d[2]:
        doc["country"] = d[2]
    if d[3]:
        doc["class_1"] = d[3]
    if d[4]:
        doc["class_2"] = d[4]
    if d[5]:
        doc["speaker"] = d[5]
    if d[7]:
        doc["outline"] = d[7]
    if d[8]:
        doc["provenance"] = d[8]

    return {"_index": "jin10", "_id": d[0], "_source": doc}


# es = Elasticsearch("wedo.com", port=9200)


def main():
    # 循环爬取并插入数据：结束条件是爬不到数据为止
    totalCount = 0
    queryParam["max_time"] = record_dict["min_time"]
    Data = requests.get(url, queryParam, headers=header).json()['data']
    length = len(Data)
    while length > 0:
        convert_data = []
        convert_docs = []
        for i in range(length):
            id = Data[i]['id']
            create_time = Data[i]['time']
            ta = time.strptime(create_time, "%Y-%m-%d %H:%M:%S")
            jid = int(time.mktime(ta)) * 10000 + int(id[14:-2])
            # create_time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            type = Data[i]['type']
            if type == 0:
                content = Data[i]['data']['content']

                l = list(parse_content(content))
                l.insert(0, create_time)
                l.insert(0, jid)

                convert_data.append(tuple(l))
                convert_docs.append(convert_es_data(l))

        # helpers.bulk(es, convert_docs)
        mysql_helper.insert_bulk(insert_template, convert_data)
        totalCount += length

        # 修正下一个查询时间
        queryParam['max_time'] = record_dict['min_time'] = Data[length - 1]['time']

        with open('record.json', 'w') as f:
            json.dump(record_dict, f, indent=4)
        logger.info('next queryParam is {}'.format(queryParam['max_time']))

        # 再请求一次数据
        # time.sleep(30)
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        Data = requests.get(url, queryParam, timeout=5, headers=header).json()['data']
        length = len(Data)

    logger.info('all ok,totalCount is:', totalCount)


def test():
    content = "创业板指跌幅收窄至1%，开盘跌超2%"
    country, class_1, class_2 = parse_flag(content)

    logger.info(country)
    logger.info(class_1)
    logger.info(class_2)


if __name__ == '__main__':
    main()
    # test()
