from helper.config_helper import get_config
from helper.argument_helper import get_arguments
from helper.download_helper import download_manga

import settings.settings as settings

import cfscrape
import logging
import sys
import os


def main(arguments):
    settings.init(arguments)

    scraper = cfscrape.create_scraper()

    for manga in settings.mangas:
        download_manga(scraper, manga)

if __name__ == '__main__':
    main(sys.argv[1:])
