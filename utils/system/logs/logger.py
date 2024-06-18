import logging, os
import sys
from configs.config import conf as config

SERVER_LOGS_FILE = os.path.join(config.BASE_DIR, config.LOG_FOLDER, 'app.log')
ERROR_LOGS_FILE = os.path.join(config.BASE_DIR, config.LOG_FOLDER, 'app.log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': config.LOG_FORMAT,
        },
        'console': {
            'format': config.LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'file': {
            'format': config.LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        "error": {
            'format': config.LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logger.handlers.RotatingFileHandler',
            'filename': SERVER_LOGS_FILE,
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 10,  # 最多备份10个
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'error': {
            'level': 'ERROR',
            'class': 'logger.handlers.RotatingFileHandler',
            'filename': ERROR_LOGS_FILE,
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 10,  # 最多备份10个
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        'console': {
            'level': 'INFO',
            'class': 'logger.StreamHandler',
            'formatter': 'console',
        }
    },
    'loggers': {
        # default日志
        '': {
            'handlers': ['console', 'error', 'file'],
            'level': 'INFO',
            # 'propagate': True,  # 是否让日志信息继续冒泡给其他的日志处理系统
        },
        'flask': {
            'handlers': ['console', 'error', 'file'],
            'level': 'INFO',
        },
        'scripts': {
            'handlers': ['console', 'error', 'file'],
            'level': 'INFO',
        },
        # 数据库相关日志
        'flask.db.backends': {
            'handlers': [],
            'propagate': True,
            'level': 'INFO',
        },
    }
}


def get_logger():
    log = logging.getLogger("log")
    log.setLevel(logging.INFO)
    return log


# 日志句柄
logger = get_logger()
