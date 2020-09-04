import pymysql
from logger import logger


class MysqlHelper():
    # 初始化属性
    def __init__(self, db_host, db_user, db_password, database):
        self.__db_host = db_host
        self.__db_port = 3306
        self.__db_user = db_user
        self.__db_password = db_password
        self.__db_database = database
        self.__db = None

    # 链接数据库
    def get_connect(self):
        self.__db = pymysql.connect(
            host=self.__db_host,
            port=self.__db_port,
            user=self.__db_user,
            password=self.__db_password,
            database=self.__db_database,
            charset='utf8'
        )

    def insert_bulk1(self, sql, insert_data):
        """
        execute(sql) : 接受一条语句从而执行
        executemany(templet,args)：能同时执行多条语句，执行同样多的语句可比execute()快很多，强烈建议执行多条语句时使用executemany
        templet : sql模板字符串,　 例如 ‘insert into table(id,name,age) values(%s,%s,%s)’
        args: 模板字符串中的参数，是一个list，在list中的每一个元素必须是元组！！！ 　例如： [(1,‘mike’),(2,‘jordan’),(3,‘james’),(4,‘rose’)]
        :param sql:
        :param insert_data:
        :return:
        """
        global cursor
        try:
            # 连接数据库
            self.get_connect()
            # 创建游标
            cursor = self.__db.cursor()
            # 执行sql命令
            cursor.executemany(sql, insert_data)
        except Exception as e:
            logger.info(e)
        finally:
            # 关闭游标
            cursor.close()
            # 提交
            self.__db.commit()
            # 关闭数据库连接
            self.__db.close()


    def insert_bulk(self, sql, insert_data):
        """
        execute(sql) : 接受一条语句从而执行
        executemany(templet,args)：能同时执行多条语句，执行同样多的语句可比execute()快很多，强烈建议执行多条语句时使用executemany
        templet : sql模板字符串,　 例如 ‘insert into table(id,name,age) values(%s,%s,%s)’
        args: 模板字符串中的参数，是一个list，在list中的每一个元素必须是元组！！！ 　例如： [(1,‘mike’),(2,‘jordan’),(3,‘james’),(4,‘rose’)]
        :param sql:
        :param insert_data:
        :return:
        """
        global cursor
        # 连接数据库
        self.get_connect()
        # 创建游标
        cursor = self.__db.cursor()
        # 执行sql命令
        cursor.executemany(sql, insert_data)
        # 关闭游标
        cursor.close()
        # 提交
        self.__db.commit()
        # 关闭数据库连接
        self.__db.close()
