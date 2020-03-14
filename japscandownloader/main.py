import cloudscraper
import sys
from jss_selenium import JapScanDownloader


if __name__ == "__main__":
    japscan_downloader = JapScanDownloader(cloudscraper.create_scraper())

    japscan_downloader.init(sys.argv[1:])

    for manga in japscan_downloader.mangas:
        japscan_downloader.download(manga)
