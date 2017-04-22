import os

import path
import ruamel.yaml


def read_config():
    cfg_path = path.Path(os.path.expanduser("~/.config/twittback.yml"))
    return ruamel.yaml.safe_load(cfg_path.text())
