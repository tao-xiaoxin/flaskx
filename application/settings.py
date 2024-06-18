import os
import sys
from pathlib import Path
from datetime import timedelta
from flask import Flask

from application.urls import init_bps
# from engine.mysql import MysqlEngine
# from . import Base

from middleware import CorsMiddleware, LoggingMiddleware

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# ================================================= #
# ******************** 动态配置 ******************** #
# ================================================= #
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "flaskx--z8%exyzt7e_%i@1+#1mm=%lb5=^fx_57=1@a+_y7bg5-w%)sm"


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

# def init_log(app):
#
#
#     # 将日志处理器添加到 Flask 的主日志处理器中
#     app.logger =
#
#     return app


def init_middleware(app):
    """
    注册中间件
    :param app:
    :return:
    """
    CorsMiddleware(app)
    LoggingMiddleware(app)


def init_db(app):
    pass


def init_plugs(app):
    pass


def init_script(app):
    pass


def create_app():
    from configs.config import BaseConfig
    app = Flask(BASE_DIR.name)
    app.config["SECRET_KEY"] = SECRET_KEY
    # 初始化配置
    app.config.from_object(BaseConfig)
    # 初始化数据库
    init_db(app)
    # 初始化中间件
    init_middleware(app)
    # 初始化插件
    init_plugs(app)
    # 初始化蓝图
    init_bps(app)
    # 初始化脚本
    init_script(app)
    return app
