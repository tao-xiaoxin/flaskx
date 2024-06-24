# encoding:utf-8
import json
import os
from utils.system.file import read_file, get_root


class Config(dict):
    """
    Config class that extends the built-in dict class in Python.
    This class is used to create a dictionary object with additional methods for convenience.
    """

    def __init__(self, d=None):
        super(Config, self).__init__()
        if d is None:
            d = {}
        for k, v in d.items():
            self[k] = v

    def __getitem__(self, key):
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        return super().__setitem__(key, value)

    def __getattr__(self, key):
        try:
            value = self[key]
            if isinstance(value, dict):
                value = Config(value)
            return value
        except KeyError:
            raise AttributeError(f"'Config' object has no attribute '{key}'")

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError as e:
            return default
        except Exception as e:
            raise e


def load_config(config_path="./config.json"):
    """
    加载默认配置文件
    :param config_path: 配置文件路径
    :return:
    """
    # from ..logs.logru import logger
    if not os.path.exists(config_path):
        # logger.info("配置文件不存在，将使用config-template.json模板")
        config_path = os.path.join(get_root(), "configs/config-template.json")
        if not os.path.exists(config_path):
            raise Exception("配置模板文件也不存在，请确保config-template.json文件存在于configs目录下")
    # logger.debug("[INIT] 当前配置文件为 {}".format(config_path))
    config_str = read_file(config_path)
    # 将json字符串反序列化为dict类型
    config = Config(json.loads(config_str))
    return config
