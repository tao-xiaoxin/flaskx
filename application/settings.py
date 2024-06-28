import json
import os
from pathlib import Path
from datetime import timedelta
from sqlalchemy.ext.declarative import declarative_base
from loguru import logger
from utils.common.tools import Dict
from utils.system.file import read_file

# import configs.config as configs
# from utils.system.logs import log as logging
# from utils.system.logs import logru

# from flask import app

# from engine.mysql import MysqlEngine
# from . import Base


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

Base = declarative_base()


def load_config(config_path="./config.json"):
    """
    加载默认配置文件
    :param config_path: 配置文件路径
    :return:
    """
    if not os.path.exists(config_path):
        logger.info("配置文件不存在，将使用config-template.json模板")
        config_path = os.path.join(BASE_DIR, "configs/config-template.json")
        if not os.path.exists(config_path):
            raise Exception("配置模板文件也不存在，请确保config-template.json文件存在于configs目录下")
    logger.debug("[INIT] 当前配置文件为 {}".format(config_path))
    config_str = read_file(config_path)
    # 将json字符串反序列化为dict类型
    config = Dict(json.loads(config_str))
    return config


# 从环境变量读取配置文件路径
CONFIG_PATH = os.getenv("CONFIG_PATH", "configs/config-template.json")

# 读取配置文件
CONFIG_INFO = load_config(config_path=CONFIG_PATH)

# 初始化plugins插件路径到环境变量中
# PLUGINS_PATH = os.path.join(BASE_DIR, "plugins")
# sys.path.insert(0, os.path.join(PLUGINS_PATH))
#
# [
#     sys.path.insert(0, os.path.join(PLUGINS_PATH, ele))
#     for ele in os.listdir(PLUGINS_PATH)
#     if os.path.isdir(os.path.join(PLUGINS_PATH, ele)) and not ele.startswith("__")
# ]
#
# # SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = locals().get("DEBUG", True)
# ALLOWED_HOSTS = locals().get("ALLOWED_HOSTS", ["*"])


# from application.common.script import init_script
# from .settings import BaseConfig
# from application.extensions import init_plugs
# from application.view import init_bps

# 初始化数据库引擎
# db_engine = MysqlEngine("default")


DEBUG = CONFIG_INFO.get('DEBUG', True)
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG_INFO.get('SECRET_KEY', "flaskx--z8%exyzt7e_%i@1+#1mm=%lb5=^fx_57=1@a+_y7bg5-w%)sm")

# ================================================= #
# ********************* 日志配置 ******************* #
# ================================================= #
# log 配置部分BEGIN
LOG_SETTINGS = CONFIG_INFO.get('log_settings', {})

LOG_FOLDER = LOG_SETTINGS.get('LOG_FOLDER', 'logs/')
LOG_ROTATION = LOG_SETTINGS.get('LOG_ROTATION', '100 MB')
LOG_RETENTION = LOG_SETTINGS.get('LOG_RETENTION', '30 days')
LOG_ENCODING = LOG_SETTINGS.get('LOG_ENCODING', 'utf-8')
LOG_BACKTRACE = LOG_SETTINGS.get('LOG_BACKTRACE', True)
LOG_DIAGNOSE = LOG_SETTINGS.get('LOG_DIAGNOSE', True)
# 格式:[日期][模块.函数名称():行号] [级别] 信息
LOG_FORMAT = LOG_SETTINGS.get('LOG_FORMAT',
                              '[%(asctime)s][%(name)s.%(funcName)s():%(lineno)d] [%(levelname)s] %(message)s')

os.makedirs(os.path.join(BASE_DIR, LOG_FOLDER), exist_ok=True)

# ================================================= #
# ********************* 数据库配置 ******************* #
# ================================================= #

# JSON配置
JSON_AS_ASCII = False
POOL_SIZE = 10
MAX_OVERFLOW = 20
POOL_RECYCLE = 1800
# SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USERNAME}:{urlquote(MYSQL_PASSWORD)}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}?charset=utf8mb4"

# 默认日志等级
# LOG_LEVEL = logger.WARN
"""
flask-mail配置
"""
# MAIL_SERVER = 'smtp.qq.com'
# MAIL_USE_TLS = False
# MAIL_USE_SSL = True
# MAIL_PORT = 465
# MAIL_USERNAME = '123@qq.com'
# MAIL_PASSWORD = 'XXXXX'  # 生成的授权码
# MAIL_DEFAULT_SENDER = MAIL_USERNAME

# 插件配置，填写插件的文件名名称，默认不启用插件。
PLUGIN_ENABLE_FOLDERS = []

# 配置多个数据库连接的连接串写法示例
# HOSTNAME: 指数据库的IP地址、USERNAME：指数据库登录的用户名、PASSWORD：指数据库登录密码、PORT：指数据库开放的端口、DATABASE：指需要连接的数据库名称
# MSSQL:    f"mssql+pymssql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=cp936"
# MySQL:    f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
# Oracle:   f"oracle+cx_oracle://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"
# SQLite    "sqlite:/// database.db"
# Postgres f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"
# Oracle的第二种连接方式
# dsnStr = cx_Oracle.makedsn({HOSTNAME}, 1521, service_name='orcl')
# connect_str = "oracle://%s:%s@%s" % ('{USERNAME}', ' {PASSWORD}', dsnStr)

#  在SQLALCHEMY_BINDS 中设置：'{数据库连接别名}': '{连接串}'
# 最后在models的数据模型class中，在__tablename__前设置        __bind_key__ = '{数据库连接别名}'  即可，表示该数据模型不使用默认的数据库连接，改用“SQLALCHEMY_BINDS”中设置的其他数据库连接
# SQLALCHEMY_BINDS = {
#    'testMySQL': 'mysql+pymysql://test:123456@192.168.1.1:3306/test?charset=utf8',
#    'testMsSQL': 'mssql+pymssql://test:123456@192.168.1.1:1433/test?charset=cp936',
#    'testOracle': 'oracle+cx_oracle://test:123456@192.168.1.1:1521/test',
#    'testSQLite': 'sqlite:///database.db'
# }
