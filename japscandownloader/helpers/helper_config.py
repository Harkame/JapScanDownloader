from yaml import Loader, load

import logging

logger = logging.getLogger(__name__)


def get_config(config_file_path):
    config_file = open(config_file_path, "r")

    config = load(config_file, Loader=Loader)

    config_file.close()

    return config
