from helpers import helper_download

import settings.settings as settings

import cloudscraper
import sys

def main(arguments):
    settings.init(arguments)

    scraper = cloudscraper.create_scraper()

    for manga in settings.mangas:
        helper_download.download_manga(scraper, manga)

if __name__ == '__main__':
    main(sys.argv[1:])
