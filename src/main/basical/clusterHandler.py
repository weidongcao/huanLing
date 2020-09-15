# -*- coding=utf-8 -*-
"""
阿里云域名解析实现家庭局域网动态域名解析
"""
import os
import json
from urllib.request import urlopen
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeSubDomainRecordsRequest import DescribeSubDomainRecordsRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest


class DnsHandler:
    # 从阿里云开发者后台获取Access_key_Id和Access_Key_secret
    access_key_id = None
    access_key_secret = None

    # 填入自己的域名
    domain_name = None

    # 填入二级域名的RR值
    rr_keyword = None

    # 解析记录类型,一般为A记录
    record_type = None

    # 用于储存解析记录的文件名
    file_name = None

    client = None
    record = None
    current_ip = ''

    # 初始化,获取client实例
    def __init__(self):
        with open("conf.json", "r", encoding="utf-8") as f:
            dt = json.load(f)
        self.access_key_id = dt["access_key_id"]
        self.access_key_secret = dt["access_key_secret"]
        self.domain_name = dt["domain_name"]
        self.rr_keyword = dt["rr_keyword"]
        self.record_type = dt["record_type"]
        self.file_name = dt["file_name"]

        self.client = AcsClient(
            self.access_key_id,
            self.access_key_secret
        )
        self.record = self.get_record()
        self.current_ip = self.get_current_ip()

    # 如果公网IP发生变化,则自动修改阿里云解析记录
    def reset(self):
        if self.current_ip != self.get_record_value():
            print(self.update_record(self.current_ip))
            self.get_record()

    # 获取阿里云域名解析完整记录,并使用文件缓存
    def get_record(self):
        if os.path.isfile(self.file_name):
            file_handler = open(self.file_name, 'r')
            r = file_handler.read()
            file_handler.close()
        else:
            request = DescribeDomainRecordsRequest()
            request.set_PageSize(10)
            request.set_action_name("DescribeDomainRecords")
            request.set_DomainName(self.domain_name)
            request.set_RRKeyWord(self.rr_keyword)
            request.set_TypeKeyWord(self.record_type)

            r = self.client.do_action_with_exception(request)
            # print(r)
            file_handler = open(self.file_name, 'wb')
            # file_handler.write(r.encode("UTF-8"))
            file_handler.write(r)
            file_handler.close()
        return json.loads(r)

    # 获取阿里云域名解析记录ID
    def get_record_id(self):
        return self.record["DomainRecords"]["Record"][0]["RecordId"]

    # 获取当前域名解析记录
    def get_record_value(self):
        return self.record["DomainRecords"]["Record"][0]["Value"]

    # 修改阿里云解析记录
    def update_record(self, value):
        request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
        request.set_action_name("UpdateDomainRecord")
        request.set_RecordId(self.get_record_id())
        request.set_Type(self.record_type)
        request.set_RR(self.rr_keyword)
        request.set_Value(value)

        return self.client.do_action_with_exception(request)

    # 获取当前公网IP
    def get_current_ip(self):
        # return json.load(urlopen('http://jsonip.com'))['ip']
        return urlopen('https://api-ipv4.ip.sb/ip').read()


# 实例化类并启动更新程序
dns = DnsHandler()
dns.reset()


