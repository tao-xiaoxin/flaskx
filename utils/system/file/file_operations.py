""" 文件操作目录相关"""
import os, yaml
from pathlib import Path


def read_file(path, mode="r", encoding="utf-8"):
    with open(path, mode=mode, encoding=encoding) as f:
        return f.read()


def get_root():
    """
    获取当前脚本的根目录。

    :return: 返回一个Path对象，表示当前脚本的根目录。
    """
    # Path(__file__).resolve() 返回一个绝对路径，表示当前文件的位置。
    # parent 属性可以获取路径的上一级目录，通过多次调用 parent，我们可以向上移动目录。
    return Path(__file__).resolve().parent.parent.parent.parent


# def get_appdata_dir():
#     data_path = os.path.join(get_root(), conf().get("appdata_dir", ""))
#     if not os.path.exists(data_path):
#         logger.info("[INIT] data path not exists, create it: {}".format(data_path))
#         os.makedirs(data_path)
#     return data_path


# def write_plugin_config(pconf: dict):
#     """
#     写入插件全局配置
#     :param pconf: 全量插件配置
#     """
#     global plugin_config
#     for k in pconf:
#         plugin_config[k.lower()] = pconf[k]


# def pconf(plugin_name: str) -> dict:
#     """
#     根据插件名称获取配置
#     :param plugin_name: 插件名称
#     :return: 该插件的配置项
#     """
#     return plugin_config.get(plugin_name.lower())
def read_yaml(config_name, config_path):
    """
    config_name:需要读取的配置内容
    config_path:配置文件路径
    """
    if config_name and config_path:
        with open(config_path, 'r', encoding='utf-8') as f:
            conf = yaml.safe_load(f.read())
        if config_name in conf.keys():
            return conf[config_name.upper()]
        else:
            raise KeyError('未找到对应的配置信息')
    else:
        raise ValueError('请输入正确的配置名称或配置文件路径')
