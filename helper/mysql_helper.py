# -*- coding:utf-8 -*-

from helper.apollo_helper import apollo_helper
from helper.db_helper import DBHelper

#################

db_type = "mysql"
mysql_conf = apollo_helper.get_value("db.mysql", namespace="airflow.yml")
mysql_helper = DBHelper(
    host=mysql_conf["host"],
    port=mysql_conf["port"],
    username=mysql_conf["user"],
    password=mysql_conf["password"],
    database=mysql_conf["database"],
    db_type=db_type
)

if __name__ == '__main__':
    val = mysql_helper.query('select version()')
    print(type(val))
    print(val)
