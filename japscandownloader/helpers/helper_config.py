import logging
import ruamel.yaml

logger = logging.getLogger(__name__)


def get_config(config_file_path):
    yaml = ruamel.yaml.YAML()

    with open(config_file_path) as fp:
        config = yaml.load(fp)

    return config


def update_config(config_file_path, manga, last_chapter):

    yaml = ruamel.yaml.YAML()

    with open(config_file_path) as fp:
        config = yaml.load(fp)

    mangas = config["mangas"]
    for item in mangas:
        if "subscription" in item:
            subscription = item["subscription"]
            if subscription["manga"] == manga:
                subscription["last_chapter"] = last_chapter
                break

    with open(config_file_path, 'w') as fp:
        yaml.dump(config, fp)

    return config
