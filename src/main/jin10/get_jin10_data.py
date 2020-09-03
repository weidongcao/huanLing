import requests
import datetime
import pymysql
import pymysql
from requests.adapters import HTTPAdapter

from elasticsearch import Elasticsearch


def conn():
    connect = pymysql.connect(host='', user='', password='', database='',charset='utf8')
    if connect:
        print("连接成功!")
    return connect
# conn = conn()

# es = Elasticsearch("wedo.com", port=9200)


##爬虫获取页面数据
url = "https://flash-api.jin10.com/get_flash_list"
header = {
    "x-app-id": "SO1EJGmNgCtmpcPF",
    "x-version": "1.0.0",
}
queryParam = {
    "max_time": "2020-07-15 16:45:02",
    "channel": "-8200",
}

#循环爬取并插入数据：结束条件是爬不到数据为止
totalCount = 0
Data = requests.get(url, queryParam, headers=header).json()['data']
length = len(Data)
while (length > 0):
    for i in range(length):
        try:
            id = Data[i]['id']
            time = Data[i]['time']
            create_time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
            type = Data[i]['type']
            if type == 0:
                if len(Data[i]['data']) > 2:
                    pic = Data[i]['data']['pic']
                    content = Data[i]['data']['content']
                    title = Data[i]['data']['title']
                elif len(Data[i]['data']) == 1:
                    pic = None
                    content = Data[i]['data']['content']
                    title = None
                else:
                    pic = Data[i]['data']['pic']
                    content = Data[i]['data']['content']
                    title = None
                print(id, time, type, pic, content, title)
                # try:
                #
                #     sql = "insert into  jin10_data(id,create_time,type,pic,content,title) values(%s,%s,%s,%s,%s,%s)"
                #     cursor = conn.cursor()
                #     cursor.execute(sql, (id, create_time, type, pic, content, title))
                #     conn.commit()
                #     cursor.close()
                # except Exception as e:
                #     print(e)
                #     continue
        except Exception as e:
            print(e)
            continue

    totalCount += length

    # 修正下一个查询时间
    queryParam['max_time'] = Data[length - 1]['time']
    print('next queryParam is', queryParam['max_time'])

    # 再请求一次数据
    try:
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        Data = requests.get(url, queryParam,timeout=5, headers=header).json()['data']
        length = len(Data)
    except Exception as e:
        print(e)



print('all ok,totalCount is:', totalCount)