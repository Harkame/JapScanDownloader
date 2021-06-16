from yaml import Loader, load, dump

import logging

logger = logging.getLogger(__name__)


def get_config(config_file_path):
    config_file = open(config_file_path, "r")

    config = load(config_file, Loader=Loader)

    config_file.close()

    return config


def update_config(config_file_path, manga, last_chapter):
    config_file = open(config_file_path, "r")
    config = load(config_file, Loader=Loader)
    config_file.close()

    mangas = config["mangas"]
    for item in mangas:
        if "subscription" in item:
            subscription = item["subscription"]
            if subscription["manga"] == manga:
                subscription["last_chapter"] = last_chapter
                break

    config_file = open(config_file_path, "w")
    dump(config, config_file)
    config_file.close()
    return config
