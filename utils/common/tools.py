"""公用的工具和方法"""

from importlib import import_module


def import_module_from_path(module_path):
    """
    从给定的模块路径导入模块。

    :param module_path: 字符串，表示要导入的模块的路径。例如，'mypackage.mymodule'。
    :return: 如果模块成功导入，返回该模块。否则，抛出异常。
    """
    try:
        # 使用Python的importlib模块的import_module函数尝试导入模块
        module = import_module(module_path)
        return module
    except ImportError:
        # 如果导入失败，抛出一个异常，包含失败的模���路径
        raise Exception(f"Module {module_path} could not be imported.")


class Dict(dict):
    """
    Config class that extends the built-in dict class in Python.
    This class is used to create a dictionary object with additional methods for convenience.
    """

    def __init__(self, d=None):
        super(Dict, self).__init__()
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
                value = Dict(value)
            return value
        except KeyError:
            raise AttributeError(f"'Dict' object has no attribute '{key}'")

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError as e:
            return default
        except Exception as e:
            raise e
