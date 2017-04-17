import os

import path
import ruamel.yaml


def read_config():
    cfg_path = path.Path(os.path.expanduser("~/.config/twittback.yml"))
    return ruamel.yaml.safe_load(cfg_path.text())


def get_auth():
    config = read_config()
    return config["auth"]


def get_db_path():
    config = read_config()
    return config["db"]["path"]
