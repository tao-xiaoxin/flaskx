import os

from utils.system.conf import load_config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 读取配置文件
CONFIG_PATH = os.path.join(BASE_DIR, "configs", "config-template.json")
CONFIG_INFO = load_config(CONFIG_PATH)
