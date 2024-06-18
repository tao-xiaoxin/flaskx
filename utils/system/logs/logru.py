import sys
from configs import conf as config
from loguru import logger as log


def setup_logging():
    """

    :return:
    """
    # 这里面采用了层次式的日志记录方式，就是低级日志文件会记录比他高的所有级别日志，这样可以做到低等级日志最丰富，高级别日志更少更关键
    # debug
    log.add(config.LOG_FOLDER + "debug.log", level="DEBUG", backtrace=config.LOG_BACKTRACE,
            diagnose=config.LOG_DIAGNOSE,
            format=config.LOG_FORMAT, colorize=False,
            rotation=config.LOG_ROTATION, retention=config.LOG_RETENTION, encoding=config.LOG_ENCODING,
            filter=lambda record: record["level"].no >= logger.level("DEBUG").no)

    # info
    log.add(config.LOG_FOLDER + "info.log", level="INFO", backtrace=config.LOG_BACKTRACE,
            diagnose=config.LOG_DIAGNOSE,
            format=config.LOG_FORMAT, colorize=False,
            rotation=config.LOG_ROTATION, retention=config.LOG_RETENTION, encoding=config.LOG_ENCODING,
            filter=lambda record: record["level"].no >= logger.level("INFO").no)

    # warning
    log.add(config.LOG_FOLDER + "warning.log", level="WARNING", backtrace=config.LOG_BACKTRACE,
            diagnose=config.LOG_DIAGNOSE,
            format=config.LOG_FORMAT, colorize=False,
            rotation=config.LOG_ROTATION, retention=config.LOG_RETENTION, encoding=config.LOG_ENCODING,
            filter=lambda record: record["level"].no >= logger.level("WARNING").no)

    # error
    log.add(config.LOG_FOLDER + "error.log", level="ERROR", backtrace=config.LOG_BACKTRACE,
            diagnose=config.LOG_DIAGNOSE,
            format=config.LOG_FORMAT, colorize=False,
            rotation=config.LOG_ROTATION, retention=config.LOG_RETENTION, encoding=config.LOG_ENCODING,
            filter=lambda record: record["level"].no >= logger.level("ERROR").no)

    # critical
    log.add(config.LOG_FOLDER + "critical.log", level="CRITICAL", backtrace=config.LOG_BACKTRACE,
            diagnose=config.LOG_DIAGNOSE,
            format=config.LOG_FORMAT, colorize=False,
            rotation=config.LOG_ROTATION, retention=config.LOG_RETENTION, encoding=config.LOG_ENCODING,
            filter=lambda record: record["level"].no >= logger.level("CRITICAL").no)

    log.add(sys.stderr, level="CRITICAL", backtrace=config.LOG_BACKTRACE, diagnose=config.LOG_DIAGNOSE,
            format=config.LOG_FORMAT, colorize=True,
            filter=lambda record: record["level"].no >= logger.level("CRITICAL").no)
    return log


logger = setup_logging()
