#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/28 10:19
# @describe: 数据库连接客户端
import pymongo
import pymysql
import redis


class Mysql:

    def __init__(self, db_config):
        """
        初始化，传参数的作用
        :param db_config: 数据库配置
        """
        self.conn = pymysql.connect(**db_config, autocommit=True)
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def execute(self, sql, args=None):
        """
        执行sql语句,返回单条数据
        :return:
        """
        try:
            self.cursor.execute(sql, args)
            return self.cursor.fetchone()
        except Exception as e:
            raise e

    def execute_all(self, sql, args=None):
        """
        执行sql语句,返回多条数据
        :param sql:
        :param args:
        :return:
        """
        try:
            self.cursor.execute(sql, args)
            return self.cursor.fetchall()
        except Exception as e:
            raise e

    def close(self):
        self.cursor.close()
        self.conn.close()
        print("关闭mysql的连接")


class MongoDB:
    def __init__(self, db_config):
        '''
        初始化mongodb数据库和表的信息，并连接数据库
        :param database: 数据库名称
        :param collection: 表
        '''
        self.client = pymongo.MongoClient(**db_config)  # 指定连接的url地址

    def find_one_collection(self, database, collection_name, *args, **kwargs):
        '''
        查询数据
        :param database:
        :param collection_name: collection名称
        :param search_col: 查询条件，只能是dict类型
        :return:
        '''
        client = self.client[database]  # 指定数据库
        my_col = client[collection_name]
        try:
            result = my_col.find_one(*args, **kwargs)
            return result
        except TypeError as e:
            raise e

    def close(self):
        self.client.close()
        print("关闭mangodb的连接")


class Redis:
    def __init__(self, db_config):
        self.host = db_config.get('host')
        self.port = db_config.get('port')
        self.conn = None

    def connect(self, database):
        '''
        传数据库名，以及端口号
        :param database:  若不用切换到 database下查询，则database 传None
        '''

        try:
            pool = redis.ConnectionPool(host=self.host, port=self.port, db=database) # 使用连接池
            self.conn = redis.Redis(connection_pool=pool, decode_responses=True)
            return self.conn
        except Exception as e:
            raise e

    def close(self):
        if self.conn is not None:
            self.conn.connection_pool.disconnect()
            print('断开redis数据库连接')


class DBClient:

    def init_connection(self, dbs):
        """
        初始化数据库连接
        :param dbs: 数据库配置
        :return:
        """
        if isinstance(dbs, list):
            for db in dbs:
                if isinstance(db, dict):
                    # 连接数据库方法
                    self.create_db_connection(db)
                else:
                    raise TypeError("数据库配置错误")
        elif isinstance(dbs, dict):
            # 连接数据库方法
            self.create_db_connection(dbs)

    def create_db_connection(self, db: dict):
        """
        创建数据库连接
        :param db: 数据库配置
        :return:
        """
        if not (db.get('name') and db.get('type') and db.get('config')):
            raise TypeError("数据库配置错误")
        if db.get('type') == 'mysql':
            setattr(self, db.get('name'), Mysql(db.get('config')))
        elif db.get('type') == 'mongodb':
            setattr(self, db.get('name'), MongoDB(db.get('config')))
        elif db.get('type') == 'redis':
            setattr(self, db.get('name'), Redis(db.get('config')))

    def close_db_connection(self):
        """关闭数据库连接"""
        for item in self.__dict__:
            if isinstance(self.__dict__[item], Mysql):
                self.__dict__[item].close()
            elif isinstance(self.__dict__[item], MongoDB):
                self.__dict__[item].close()
            elif isinstance(self.__dict__[item], Redis):
                self.__dict__[item].close()


if __name__ == '__main__':
    db = [
        {
            "name": "learn",
            "type": "mysql",
            "config": {
                "host": "127.0.0.1",
                "port": 3306,
                "user": "root",
                "password": "123456"
            }
        },
        {
            "name": "webcomics",
            "type": "mysql",
            "config": {
                "host": "127.0.0.1",
                "port": 3306,
                "user": "root",
                "password": "123456"
            }
        },
        {
            "name": "mango",
            "type": "mongodb",
            "config": {
                "host": "18.162.188.202",
                "port": 10207
            }
        },
        {
            "name": "red",
            "type": "redis",
            "config": {
                "host": "18.162.188.202",
                "port": 6379
            }
        }
    ]
    db2 = DBClient()
    db2.init_connection(db)
    res = db2.learn.execute_all("select * from apptest.usermodel")
    print(res)
    res2 = db2.webcomics.execute_all("select * from apptest.postmodel")
    print(res2)

    print("连接mangodb数据库测试")
    res3 = db2.mango.find_one_collection('mangaBox', "book", {"name": "The Law of Yama"})
    print(res3)
    print("连接redis数据库测试")
    con = db2.red.connect(database="2")
    res4 = con.get("1000000000000001")
    print(res4)
    db2.close_db_connection()
