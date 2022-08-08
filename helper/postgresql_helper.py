# -*- coding:utf-8 -*-

from helper.apollo_helper import apollo_helper
from helper.db_helper import DBHelper

#################

db_type = "postgresql"
postgre_conf = apollo_helper.get_value("db.pg", namespace="commons.yml")
postgres_helper = DBHelper(
    host=postgre_conf["host"],
    port=str(postgre_conf["port"]),
    username=postgre_conf["user"],
    password=postgre_conf["password"],
    database=postgre_conf["database"],
    db_type=db_type
)

if __name__ == '__main__':
    val = postgres_helper.query('select version()')
    print(type(val))
    print(val)
