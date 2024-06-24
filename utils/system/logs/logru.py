import sys
from loguru import logger
from application import settings

# This code uses a hierarchical logging method, where lower-level log files will record all logs of higher levels.
# This way, lower-level logs are the most abundant, and higher-level logs are fewer and more critical.


# Add a debug level logger
logger.add(settings.LOG_FOLDER + "debug.log", level="DEBUG", backtrace=settings.LOG_BACKTRACE,
           diagnose=settings.LOG_DIAGNOSE,
           format=settings.LOG_FORMAT, colorize=False,
           rotation=settings.LOG_ROTATION, retention=settings.LOG_RETENTION, encoding=settings.LOG_ENCODING,
           filter=lambda record: record["level"].no >= logger.level(
               "DEBUG").no)  # Only logs of level DEBUG or higher will be recorded

# Add an info level logger
logger.add(settings.LOG_FOLDER + "info.log", level="INFO", backtrace=settings.LOG_BACKTRACE,
           diagnose=settings.LOG_DIAGNOSE,
           format=settings.LOG_FORMAT, colorize=False,
           rotation=settings.LOG_ROTATION, retention=settings.LOG_RETENTION, encoding=settings.LOG_ENCODING,
           filter=lambda record: record["level"].no >= logger.level(
               "INFO").no)  # Only logs of level INFO or higher will be recorded

# Add a warning level logger
logger.add(settings.LOG_FOLDER + "warning.log", level="WARNING", backtrace=settings.LOG_BACKTRACE,
           diagnose=settings.LOG_DIAGNOSE,
           format=settings.LOG_FORMAT, colorize=False,
           rotation=settings.LOG_ROTATION, retention=settings.LOG_RETENTION, encoding=settings.LOG_ENCODING,
           filter=lambda record: record["level"].no >= logger.level(
               "WARNING").no)  # Only logs of level WARNING or higher will be recorded

# Add an error level logger
logger.add(settings.LOG_FOLDER + "error.log", level="ERROR", backtrace=settings.LOG_BACKTRACE,
           diagnose=settings.LOG_DIAGNOSE,
           format=settings.LOG_FORMAT, colorize=False,
           rotation=settings.LOG_ROTATION, retention=settings.LOG_RETENTION, encoding=settings.LOG_ENCODING,
           filter=lambda record: record["level"].no >= logger.level(
               "ERROR").no)  # Only logs of level ERROR or higher will be recorded

# Add a critical level logger
logger.add(settings.LOG_FOLDER + "critical.log", level="CRITICAL", backtrace=settings.LOG_BACKTRACE,
           diagnose=settings.LOG_DIAGNOSE,
           format=settings.LOG_FORMAT, colorize=False,
           rotation=settings.LOG_ROTATION, retention=settings.LOG_RETENTION, encoding=settings.LOG_ENCODING,
           filter=lambda record: record["level"].no >= logger.level(
               "CRITICAL").no)  # Only logs of level CRITICAL or higher will be recorded

# Add a logger for critical level logs to stderr
logger.add(sys.stderr, level="CRITICAL", backtrace=settings.LOG_BACKTRACE, diagnose=settings.LOG_DIAGNOSE,
           format=settings.LOG_FORMAT, colorize=True,
           filter=lambda record: record["level"].no >= logger.level(
               "CRITICAL").no)  # Only logs of level CRITICAL or higher will be recorded
