import sys
from jss_selenium import JapScanDownloader
import signal

if __name__ == "__main__":
    jsl = JapScanDownloader()

    signal.signal(signal.SIGINT, jsl.signal_handler)

    jsl.init(sys.argv[1:])

    for manga in jsl.mangas:
        jsl.download(manga)
