# -*- coding:utf-8 -*-

# import clickhouse_driver
# import psycopg2
import logging

import psycopg2
import pymysql

logger = logging.getLogger(__name__)

class DBHelper:
    """
    数据库连接工具类
    """

    def __init__(self, host, port, username, password, database, url=None, charset="utf8", db_type="mysql"):
        self.host = host
        self.port = str(port)
        self.username = username
        self.password = password
        self.database = database
        self.charset = charset
        self.db_type = db_type
        self.cursor = None
        self.conn = None
        self.url = url
        self.get_client()

    def query(self, sql, clz=list):
        """
        查询返回多条数据
        可以指定返回类型,
        默认为list,不包含字段名
        也可以指定返回类型为json或者自定义对象
        返回列表
        :param clz:
        :param sql:
        :return:
        """
        try:
            self.cursor.execute(sql)

            return self.cursor.fetchall() if list == clz else self.convert2entity(clz)
        except Exception as e:
            logger.error('SQL: %s, Error: %s ' % (sql, e))

    def query_one(self, sql, clz=tuple):
        """
        查询单条数据,
        返回指定的对象类型
        :param sql:
        :param clz:
        :return:
        """
        lt = self.query(sql, clz=list) if clz == tuple else self.query(sql, clz)

        return lt[0] if lt else None

    def modify(self, sql):
        """
        修改数据库,包括插入,更新,删除
        :param sql:
        :return:
        """
        try:
            self.cursor.execute(sql)
            self.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(sql,e)
            logger.error('SQL: %s, Error: %s ' % (sql, e))
            return False

    def insert(self, sql):
        """
        插入数据
        """
        result = self.modify(sql)
        logger.info(f"insert success --> {result}")
        return result

    def delete(self, sql):
        """
        删除数据
        :param sql:
        :return:
        """
        result = self.modify(sql)
        logger.info(f"delete success --> {result}")
        return result

    def update(self, sql):
        """
        更新数据
        :param sql:
        :return:
        """
        result = self.modify(sql)
        logger.info(f"update success --> {result}")
        return result

    def insert_bulk(self, sql, insert_data):
        """
        execute(sql) : 接受一条语句从而执行
        executemany(template,args)：能同时执行多条语句，执行同样多的语句可比execute()快很多，强烈建议执行多条语句时使用executemany
        template : sql模板字符串,　 例如 ‘insert into table(id,name,age) values(%s,%s,%s)’
        args: 模板字符串中的参数，是一个list，在list中的每一个元素必须是元组！！！ 　例如： [(1,‘mike’),(2,‘jordan’),(3,‘james’),(4,‘rose’)]
        :param sql:
        :param insert_data:
        :return:
        """
        if len(insert_data) == 0:
            logger.warning("empty insert data list, sql: {}".format(sql))
            return

        try:

            # # 连接数据库
            # self.get_connect()
            # 执行sql命令
            result  = self.conn.cursor().executemany(sql, insert_data)
            self.commit()
            print(result)
        except Exception as e:
            print(e)
            self.conn.rollback()
            logger.info(e)
            raise e

    def commit(self):
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def get_client(self):
        if "mysql" == self.db_type:
            connection = pymysql.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database,
                port=int(self.port),
                charset=self.charset
            )
            self.conn = connection
            self.cursor = self.conn.cursor()
        elif "postgresql" == self.db_type:
            connection = psycopg2.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                database=self.database,
                port=self.port
            )
            self.conn = connection
            self.cursor = self.conn.cursor()
        elif "clickhouse" == self.db_type:
            # connection = clickhouse_driver.Client(
            #     host=self.host,
            #     user=self.username,
            #     password=self.password,
            #     database=self.database,
            #     port=self.port,
            # )
            # self.conn = connection
            pass

        self.cursor.execute("SELECT VERSION()")
        r = self.cursor.fetchone()
        logger.info(r)
        logger.info(f"{self.db_type} connection init success")

    def convert2entity(self, clz=None):
        """
        如果类型什么都不传只返回值
        如果类型为基本数据类型返回单个值
        如果指定类型转为指定的类型
        :return:
        """
        keys = [c[0] for c in self.cursor.description]
        values = [e for e in self.cursor.fetchall()]
        if clz in [str, int, float, bool]:
            lt = [e[0] for e in values]
            return lt
        elif clz is None:
            return values
        else:
            return [clz(**dict(zip(keys, row))) for row in values]
