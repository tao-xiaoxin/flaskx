import os,json

from utils.common.tools import Dict
from utils.system.file import read_file

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_config(config_path="./config.json"):
    """
    加载默认配置文件
    :param config_path: 配置文件路径
    :return:
    """
    from utils.system.logs.logru import logger
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


# 读取配置文件
CONFIG_PATH = os.path.join(BASE_DIR, "configs", "config-template.json")
CONFIG_INFO = load_config(CONFIG_PATH)
