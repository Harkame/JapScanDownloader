from helper.download_helper import download_manga

import settings.settings as settings

import cfscrape
import sys

def main(arguments):
    settings.init(arguments)

    scraper = cfscrape.create_scraper()

    for manga in settings.mangas:
        download_manga(scraper, manga)

if __name__ == '__main__':
    main(sys.argv[1:])
