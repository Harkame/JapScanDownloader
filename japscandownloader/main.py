import sys
from jss_selenium import JapScanDownloader

if __name__ == "__main__":
    jsl = JapScanDownloader()

    jsl.init(sys.argv[1:])

    for manga in jsl.mangas:
        jsl.download(manga)
