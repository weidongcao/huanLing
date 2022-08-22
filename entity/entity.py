# -*- coding:utf-8 -*-
"""
存储所有的实体信息
"""
import json
import logging
from collections import namedtuple
from datetime import datetime

from dateutil.relativedelta import relativedelta
from requests import Response

logger = logging.getLogger(__name__)

DATE_FORMAT = "%Y-%m-%d %H::%M:%S"


class Entity(object):
    """
    通用实体类
    """
    table_name = ''
    id = "id"

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def __getattr__(self, column_name):
        logger.error(f"没有该属性:{column_name}")
        # return self.__dict__.get(column_name)
        return None

    def __setattr__(self, key, value):
        return self.__setattr__(key, value)


class HttpEntity(object):
    def __init__(self, status_code=None, title=None, type=None, detail=None, **kwargs):
        # super().__init__(**kwargs)
        self.status_code = status_code
        self.title = title
        self.type = type
        self.detail = detail
        self.__dict__.update(**kwargs)

        if "status" in kwargs and not self.status_code:
            self.status_code = kwargs.get("status")

    @staticmethod
    def parse_response(response: Response, cls=dict):
        e = json.loads(response.text)
        instance = cls(**e)
        if hasattr(instance, "status_code"):
            setattr(instance, "status_code", response.status_code)
        elif hasattr(instance, "response_code"):
            setattr(instance, "response_code", response.status_code)
        return instance

    def message(self, column_value_type="not_null", indent=4, ensure_ascii=False):
        dt = dict()
        if "all" == column_value_type:
            dt = self.__dict__
        elif "not_null" == column_value_type or "not_none" == column_value_type.lower():
            for k, v in self.__dict__.items():
                if v:
                    dt[k] = v
        return json.dumps(dt, indent=indent, ensure_ascii=ensure_ascii, cls=DateEncoder)


# 测试类
User = namedtuple("User", ["name", "age", "gender"])


class DateEncoder(json.JSONEncoder):
    def default(self, obj, date_format="%Y-%m-%d %H:%M:%S"):
        if isinstance(obj, datetime):
            return obj.strftime(date_format)
        elif isinstance(obj, relativedelta):
            return obj.normalized()
        else:
            return json.JSONEncoder.default(self, obj)


def get_sql_insert(table_name: str, info, auto_increase_id=None):
    """
    根据表名,数据(dict)生成生成
    排除自动递增的字段,默认只有1个字段
    :param table_name:  表名
    :param info: 需要插入的数据,可以是1条数据,类型必须是字典;也可以是列表,元素必须是字典
    :param auto_increase_id: 自动递增的字段
    :return: insert语句
    """
    # 如果表名或者数据为空,返回
    if (not table_name) or (not info):
        logger.warning(f"table_name or data is empty, table name: {table_name}; data: {info}")
        return None

    # 排除自动递增的字段
    if auto_increase_id:
        del info[auto_increase_id]

    insert_data = []
    if type(info) == dict:
        info = [info]

    columns = info[0].keys()
    # insert sql
    s = ", ".join(["%s"] * len(columns))
    insert_sql = f"insert into {table_name}({', '.join(columns)}) values ({s})"
    for dt in info:
        record = [dt[col] for col in columns]
        insert_data.append(record)

    return insert_sql, insert_data
