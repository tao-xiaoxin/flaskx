# coding: utf-8

import pymysql
from dbutils.pooled_db import PooledDB, SharedDBConnection
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from application import settings


# class MysqlEngine:
#     def __init__(self, db_name):
#         """
#         初始化数据库连接
#         """
#         db_config = settings.MYSQL_DATABASES[db_name]
#
#         self.connection_string = (
#             f"mysql+pymysql://{db_config['USER']}:{db_config['PASSWORD']}"
#             f"@{db_config['HOST']}:{db_config['PORT']}/{db_config['DB']}?charset={db_config['charset']}"
#         )
#         self.engine = create_engine(
#             self.connection_string,
#             poolclass=QueuePool,
#             pool_size=config.POOL_SIZE,
#             max_overflow=config.MAX_OVERFLOW,
#             pool_recycle=config.POOL_RECYCLE,
#         )
#         self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
#
#
#     def session(self):
#         return self.session_local()
#

class PyMySQLConnectionPool:

    def __init__(self, db_name):
        self.pool = PooledDB(
            creator=pymysql,    # 使用链接数据库的模块
            maxconnections=10,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=5,        # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=20,       # 链接池中最多闲置的链接，0和None不限制
            maxshared=3,        # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql的threadsafety为1，所有链接都是独享的。
            blocking=True,      # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,      # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],      # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=1,
            # ping MySQL服务端，检查是否服务可用。如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is
            # created, 4 = when a query is executed, 7 = always
            host=config.MYSQL_DATABASES[db_name]['host'],
            port=config.MYSQL_DATABASES[db_name]['port'],
            user=config.MYSQL_DATABASES[db_name]['user'],
            password=config.MYSQL_DATABASES[db_name]['password'],
            database=config.MYSQL_DATABASES[db_name]['db'],
            charset=config.MYSQL_DATABASES[db_name]['charset']
        )

    def open(self):
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor()
        return self.conn, self.cursor

    def get_connection(self):
        return self.pool.connection()

    def close(self, cursor, conn):
        cursor.close()
        conn.close()

    def select_one(self, sql):
        """查询单条数据"""
        conn, cursor = self.open()
        cursor.execute(sql)
        result = cursor.fetchone()
        self.close(conn, cursor)
        return result

    def select_all(self, sql):
        """查询多条数据"""
        conn, cursor = self.open()
        cursor.execute(sql)
        result = cursor.fetchall()
        self.close(conn, cursor)
        return result

    def insert_one(self, sql):
        """插入单条数据"""
        self.execute(sql, isNeed=False)

    def insert_one_2(self, sql, data):
        """插入单条数据"""
        self.execute2(sql, data, isNeed=False)

    def insert_all(self, sql, datas):
        """插入多条批量插入"""
        conn, cursor = self.open()
        try:
            cursor.executemany(sql, datas)
            conn.commit()
            return {'result': True, 'id': int(cursor.lastrowid)}
        except Exception as err:
            conn.rollback()
            return {'result': False, 'err': err}

    def update_one(self, sql):
        """更新数据"""
        self.execute(sql, isNeed=True)

    def delete_one(self, sql):
        """删除数据"""
        self.execute(sql, isNeed=True)

    def execute(self, sql, isNeed=False):
        """
        执行
        :param sql
        :param isNeed 是否需要回滚
        """
        conn, cursor = self.open()
        if isNeed:
            try:
                cursor.execute(sql)
                conn.commit()
            except:
                conn.rollback()
        else:
            cursor.execute(sql)
            conn.commit()
        self.close(conn, cursor)

    def execute2(self, sql, data, isNeed=False):
        """
        执行
        :param sql
        :param isNeed 是否需要回滚
        """
        conn, cursor = self.open()
        if isNeed:
            try:
                cursor.execute(sql, data)
                conn.commit()
            except:
                conn.rollback()
        else:
            cursor.execute(sql, data)
            conn.commit()
        self.close(conn, cursor)

    def show_tables(self):
        conn, cursor = self.open()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        return tables

    def show_table_columns(self, table_name):
        conn, cursor = self.open()
        cursor.execute(f"SHOW FULL COLUMNS FROM `{table_name}`;")
        columns = cursor.fetchall()
        return columns


QAPyMySQLConn = PyMySQLConnectionPool("flaskx")
