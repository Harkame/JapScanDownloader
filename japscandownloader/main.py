import cfscrape
import errno

from helper.config_helper import get_config
from helper.argument_helper import get_arguments
from helper.download_helper import download_manga

import sys
import os

import settings.settings as settings
import logging #logs

DEFAULT_CONFIG_FILE = os.path.join('.', 'config.yml')
DEFAULT_DESTINATION_PATH = os.path.join('.', 'mangas')
DEFAULT_MANGA_FORMAT = 'jpg'

def main():
    settings.init()

    settings.config_file = DEFAULT_CONFIG_FILE

    arguments = get_arguments(sys.argv[1:])

    if arguments.verbose:
        settings.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(module)s :: %(lineno)s :: %(funcName)s :: %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        if arguments.verbose == 0:
            settings.logger.setLevel(logging.NOTSET)
        elif arguments.verbose == 1:
            settings.logger.setLevel(logging.DEBUG)
        elif arguments.verbose == 2:
            settings.logger.setLevel(logging.INFO)
        elif arguments.verbose == 3:
            settings.logger.setLevel(logging.WARNING)
        elif arguments.verbose == 4:
            settings.logger.setLevel(logging.ERROR)
        elif arguments.verbose == 5:
            settings.logger.setLevel(logging.CRITICAL)

        settings.logger.addHandler(stream_handler)

    if arguments.config_file:
        settings.config_file = arguments.config_file

    if arguments.destination_path:
        settings.destination_path = arguments.destination_path

    if arguments.format:
        settings.manga_format = arguments.format

    if arguments.remove:
        remove = arguments.remove

    config = get_config(settings.config_file)

    mangas = []

    if config['mangas'] is not None:
        mangas = config['mangas']

    if settings.destination_path is None:
        if config['destinationPath'] is not None:
            settings.destination_path = config['destinationPath']
        else:
            settings.destination_path = DEFAULT_DESTINATION_PATH

    if settings.manga_format is None:
        if config['mangaFormat'] is not None:
            settings.manga_format = config['mangaFormat']
        else:
            settings.manga_format = DEFAULT_MANGA_FORMAT

    settings.logger.debug('mangas : %s', mangas)
    settings.logger.debug('settings : %s', settings)
    settings.logger.debug('settings.manga_format : %s', settings.manga_format)
    settings.logger.debug('remove : %s', remove)

    scraper = cfscrape.create_scraper()

    for manga in mangas:
        download_manga(scraper, manga)

if __name__ == '__main__':
    main()
