import config.config as config

from yaml import Loader, load #config file

def get_config():
    if config.config_file is None:
        config.config_file = config.DEFAULT_CONFIG_FILE

    config_stream = open(config.config_file, 'r')

    config_file = load(config_stream, Loader=Loader)

    config_stream.close()

    if config_file['mangas'] is not None:
        config.mangas.extend(config_file['mangas'])

    if config.destination_path is None:
        if config_file['destinationPath'] is not None:
            config.destination_path = config_file['destinationPath']
        else:
            config.destination_path = config.DEFAULT_DESTINATION_PATH

    if config.manga_format is None:
        if config_file['mangaFormat'] is not None:
            config.manga_format = config_file['mangaFormat']
        else:
            config.manga_format = config.DEFAULT_MANGA_FORMAT
