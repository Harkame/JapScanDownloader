import sys
from .jss_selenium import JapScanDownloader


def main():
    jsd = JapScanDownloader()

    jsd.init(sys.argv[1:])

    for manga in jsd.mangas:
        jsd.download(manga)


if __name__ == "__main__":
    main()
