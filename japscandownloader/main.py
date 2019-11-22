from helpers import download

import settings

import cloudscraper
import sys


def main(arguments):
    settings.init(arguments)

    scraper = cloudscraper.create_scraper()

    html = scraper.get("https://www.japscan.co/")

    print(html)

    return

    for manga in settings.mangas:
        download(scraper, manga)


if __name__ == "__main__":
    main(sys.argv[1:])
