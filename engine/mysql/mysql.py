# coding: utf-8

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from configs.config import conf as config
from dbutils.pooled_db import PooledDB
from pymysql.cursors import DictCursor
from timeit import default_timer


class MysqlEngine:
    def __init__(self, db_name):
        """
        初始化数据库连接
        """
        db_config = config.DATABASES[db_name]

        self.connection_string = (
            f"mysql+pymysql://{db_config['USER']}:{db_config['PASSWORD']}"
            f"@{db_config['HOST']}:{db_config['PORT']}/{db_config['db']}?charset={db_config['charset']}"
        )
        self.engine = create_engine(
            self.connection_string,
            poolclass=QueuePool,
            pool_size=config.POOL_SIZE,
            max_overflow=config.MAX_OVERFLOW,
            pool_recycle=config.POOL_RECYCLE,
        )
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def session(self):
        return self.session_local()


#

class PyMySQLConnectionPool:
    """

    """

    def __init__(self, db_name):
        self.pool = PooledDB(
            creator=pymysql,  # 使用链接数据库的模块
            maxconnections=10,  # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=5,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            maxcached=20,  # 链接池中最多闲置的链接，0和None不限制
            maxshared=3,  # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql的threadsafety为1，所有链接都是独享的。
            blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
            setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            ping=1,
            # ping MySQL服务端，检查是否服务可用。如：0 = None = never, 1 = default = whenever it is requested, 2 = when a cursor is
            # created, 4 = when a query is executed, 7 = always
            host=config.MYSQL_DATABASES[db_name]['HOST'],
            port=config.MYSQL_DATABASES[db_name]['PORT'],
            user=config.MYSQL_DATABASES[db_name]['USER'],
            password=config.MYSQL_DATABASES[db_name]['PASSWORD'],
            database=config.MYSQL_DATABASES[db_name]['DB'],
            charset=config.MYSQL_DATABASES[db_name]['CHARSET']
        )

    # def __init__(self) -> None:
    #     self.__host = "自己的host"
    #     self.__port = 3306
    #     self.__user = "自己的user"
    #     self.__password = "自己的密码"
    #     self.__database = "自己的数据库"
    #     self._log_time = True
    #     self._log_label = "总用时"
    #     self.connects_pool = DB_MySQL_Pool(
    #         host=self.__host, port=self.__port, user=self.__user, password=self.__password, database=self.__database)

    # def __enter__(self):
    #     # 如果需要记录时间
    #     if self._log_time is True:
    #         self._start = default_timer()
    #
    #     connect = self.connects_pool.get_connect()
    #     cursor = connect.cursor(pymysql.cursors.DictCursor)
    #     # https://blog.51cto.com/abyss/1736844
    #     # connect.autocommit = False # 如果使用连接池 则不能在取出后设置 而应该在创建线程池时设置
    #     self._connect = connect
    #     self._cursor = cursor
    #     return self

    # def __exit__(self, *exc_info):
    #     self._connect.commit()
    #     self._cursor.close()
    #     self._connect.close()
    #
    #     if self._log_time is True:
    #         diff = default_timer() - self._start
    #         print('-- %s: %.6f 秒' % (self._log_label, diff))

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


# QAPyMySQLConn = PyMySQLConnectionPool("flaskx")
class DB_MySQL_Pool:
    """db连接池"""
    __pool = None
    __MAX_CONNECTIONS = 100  # 创建连接池的最大数量
    __MIN_CACHED = 10  # 连接池中空闲连接的初始数量
    __MAX_CACHED = 20  # 连接池中空闲连接的最大数量
    __MAX_SHARED = 10  # 共享连接的最大数量
    __BLOCK = True  # 超过最大连接数量时候的表现，为True等待连接数量下降，为false直接报错处理
    __MAX_USAGE = 100  # 单个连接的最大重复使用次数
    __CHARSET = 'UTF8mb4'
    '''
        set_session:可选的SQL命令列表，可用于准备
                    会话，例如[“将日期样式设置为...”，“设置时区...”]
                    重置:当连接返回池中时，应该如何重置连接
                    (False或None表示回滚以begin()开始的事务，
                    为安全起见，始终发出回滚命令)
    '''
    __RESET = True
    __SET_SESSION = ['SET AUTOCOMMIT = 1']  # 设置自动提交

    def __init__(self, host, port, user, password, database):
        if not self.__pool:
            self.__class__.__pool = PooledDB(creator=pymysql, host=host, port=port, user=user, password=password,
                                             database=database,
                                             maxconnections=self.__MAX_CONNECTIONS,
                                             mincached=self.__MIN_CACHED,
                                             maxcached=self.__MAX_CACHED,
                                             maxshared=self.__MAX_SHARED,
                                             blocking=self.__BLOCK,
                                             maxusage=self.__MAX_USAGE,
                                             setsession=self.__SET_SESSION,
                                             reset=self.__RESET,
                                             charset=self.__CHARSET)

    def get_connect(self):
        return self.__pool.connection()
