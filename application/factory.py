from application.urls import init_bps
from middleware import CorsMiddleware, LoggingMiddleware


def init_middleware(app):
    """
    注册中间件
    :param app:
    :return:
    """
    CorsMiddleware(app)
    LoggingMiddleware(app)


def init_log(app):
    ...


def init_db(app):
    pass


def init_plugs(app):
    pass


def init_script(app):
    pass


# def init_log(app):
#     """
#     初始化日志
#     :param app:
#     :return:
#     """
#     logger = loguru.get_logger(app.config)
#     # logger.get_logger(app.config)
#     logger.info("日志初始化成功")
#     return logger


def init_app(app):
    # 初始化配置
    app.config.from_pyfile("application/settings.py")  # 配置文件与当前文件处于同一级
    # 初始化日志
    init_log(app)
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

