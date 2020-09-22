# -*- coding=utf-8 -*-
import json
import logging
import os
from urllib.request import urlopen

from aliyunsdkalidns.request.v20150109 import UpdateDomainRecordRequest
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordsRequest import DescribeDomainRecordsRequest
from aliyunsdkcore.client import AcsClient
from logger import logger


class DnsHandler:
    """
    阿里云域名解析实现家庭局域网动态域名解析
    """
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
        with open(os.path.join(os.path.dirname(__file__), "aliCloud.json"), "r", encoding="utf-8") as f:
            dt = json.load(f)
        self.access_key_id = dt["access_key_id"]
        self.access_key_secret = dt["access_key_secret"]
        self.domain_name = dt["domain_name"]
        self.rr_keyword = dt["rr_keyword"]
        logger.info("nomain name --> {}.{}".format(self.rr_keyword, self.domain_name))
        self.record_type = dt["record_type"]
        self.file_name = dt["file_name"]

        self.client = AcsClient(
            self.access_key_id,
            self.access_key_secret
        )
        self.record = self.get_record()
        self.current_ip = self.get_current_ip()
        logger.info("current IP address --> {}".format(self.current_ip))

    def reset(self):
        """
        阿里云不允许修改相同的解析，所以需要比对IP是否一致
        如果公网IP发生变化,则自动修改阿里云解析记录
        :return:
        """
        if self.current_ip != self.get_record_value():
            logger.info("your IP address has changed")
            logger.info("begin to update mapping to domain name")
            self.update_record()
            self.get_record()
        else:
            logger.info("your IP address doesn't change")

    # 获取阿里云域名解析完整记录,并使用文件缓存
    def get_record(self):
        if os.path.isfile(self.file_name):
            with open(self.file_name, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            desc =  self.domain_desc()
            self.write_domain_desc(desc)
            return desc

    def domain_desc(self, operate_type='get'):
        """
        get domain name describle from ali cloud
        :return:
        """
        request = DescribeDomainRecordsRequest()
        # request.set_accept_format("json")
        request.set_PageSize(10)
        request.set_action_name("DescribeDomainRecords")
        request.set_DomainName(self.domain_name)
        request.set_RRKeyWord(self.rr_keyword)
        request.set_TypeKeyWord(self.record_type)

        aa = self.client.do_action_with_exception(request)
        r = json.loads(aa.decode())
        logger.info("{} domain name describe success --> {}".format(operate_type, json.dumps(r, indent=4, ensure_ascii=False, sort_keys=True)))
        return r

    def write_domain_desc(self, domain_desc):
        with open(self.file_name, 'w', encoding='utf-8') as f:
            json.dump(domain_desc, f, indent=4, ensure_ascii=False, sort_keys=True)
        logger.info("write into domain name desc into file success --> {}".format(self.file_name))

    # 获取阿里云域名解析记录ID
    def get_record_id(self):
        return self.record["DomainRecords"]["Record"][0]["RecordId"]

    # 获取当前域名解析记录
    def get_record_value(self):
        original_ip = self.record["DomainRecords"]["Record"][0]["Value"]
        logger.info("original IP address --> {}".format(original_ip))
        return original_ip

    # 修改阿里云解析记录
    def update_record(self):
        request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
        request.set_action_name("UpdateDomainRecord")
        request.set_RecordId(self.get_record_id())
        request.set_Type(self.record_type)
        request.set_RR(self.rr_keyword)
        request.set_Value(self.current_ip)

        r = json.loads(self.client.do_action_with_exception(request).decode())
        logger.info(json.dumps(r, indent=4, ensure_ascii=True))
        logger.info("update domain name mapping success : {} --> {}.{}".format(self.current_ip, self.rr_keyword, self.domain_name))
        desc =  self.domain_desc("update")
        self.write_domain_desc(desc)
        return desc

    # 获取当前公网IP
    @staticmethod
    def get_current_ip():
        ip = urlopen('https://api-ipv4.ip.sb/ip').read().decode().replace('\n', '').replace('\r', '')
        return ip


if __name__ == '__main__':
    # 实例化类并启动更新程序
    dns = DnsHandler()
    # dns.domain_desc()
    dns.reset()
    # dns.domain_desc("get")
    # clt = AcsClient("LTAI4GAYRiAArDQyT186ZsJM", "vU7Vagyp21LnDR4DZxmCfFNgV6Jpbo")
    # DomainRecords = DescribeDomainRecordsRequest()
    # DomainRecords.set_accept_format('json')
    # DomainRecords.set_DomainName("caoweidong.cn")
    # result = json.loads(clt.do_action_with_exception(DomainRecords))
    # print(result)
