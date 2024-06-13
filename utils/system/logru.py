import sys

from loguru import logger

from configs import config


# 这里面采用了层次式的日志记录方式，就是低级日志文件会记录比他高的所有级别日志，这样可以做到低等级日志最丰富，高级别日志更少更关键
# debug
logger.add(config.lOG_FOLDER + "debug.log", level="DEBUG", backtrace=config.LOG_BACKTRACE, diagnose=config.LOG_DIAGNOSE,
           format=config.LOG_FORMAT, colorize=False,
           rotation=config.LOG_ROTATION, retention=config.LOG_RETENTION, encoding=config.LOG_ENCODING,
           filter=lambda record: record["level"].no >= logger.level("DEBUG").no)

# info
logger.add(config.lOG_FOLDER + "info.log", level="INFO", backtrace=config.LOG_BACKTRACE, diagnose=config.LOG_DIAGNOSE,
           format=config.LOG_FORMAT, colorize=False,
           rotation=config.LOG_ROTATION, retention=config.LOG_RETENTION, encoding=config.LOG_ENCODING,
           filter=lambda record: record["level"].no >= logger.level("INFO").no)

# warning
logger.add(config.lOG_FOLDER + "warning.log", level="WARNING", backtrace=config.LOG_BACKTRACE, diagnose=config.LOG_DIAGNOSE,
           format=config.LOG_FORMAT, colorize=False,
           rotation=config.LOG_ROTATION, retention=config.LOG_RETENTION, encoding=config.LOG_ENCODING,
           filter=lambda record: record["level"].no >= logger.level("WARNING").no)

# error
logger.add(config.lOG_FOLDER + "error.log", level="ERROR", backtrace=config.LOG_BACKTRACE, diagnose=config.LOG_DIAGNOSE,
           format=config.LOG_FORMAT, colorize=False,
           rotation=config.LOG_ROTATION, retention=config.LOG_RETENTION, encoding=config.LOG_ENCODING,
           filter=lambda record: record["level"].no >= logger.level("ERROR").no)

# critical
logger.add(config.lOG_FOLDER + "critical.log", level="CRITICAL", backtrace=config.LOG_BACKTRACE, diagnose=config.LOG_DIAGNOSE,
           format=config.LOG_FORMAT, colorize=False,
           rotation=config.LOG_ROTATION, retention=config.LOG_RETENTION, encoding=config.LOG_ENCODING,
           filter=lambda record: record["level"].no >= logger.level("CRITICAL").no)

logger.add(sys.stderr, level="CRITICAL", backtrace=config.LOG_BACKTRACE, diagnose=config.LOG_DIAGNOSE,
           format=config.LOG_FORMAT, colorize=True,
           filter=lambda record: record["level"].no >= logger.level("CRITICAL").no)
