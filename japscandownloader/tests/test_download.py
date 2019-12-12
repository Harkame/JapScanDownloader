import os

import unittest
import cloudscraper

from ..japscandownloader import JapScanDownloader

import shutil


class TestDownload(unittest.TestCase):
    japscandownloader = JapScanDownloader(cloudscraper.create_scraper())

    def setUp(self):
        self.japscandownloader.manga_format = "png"
        self.japscandownloader.destination_path = os.path.join(
            os.path.dirname(__file__), "test_download"
        )

        if not os.path.exists(self.japscandownloader.destination_path):
            os.makedirs(self.japscandownloader.destination_path)

    def test_download_manga(self):
        mangas = {"url": "https://www.japscan.co/manga/raba-the-mules/"}

        self.japscandownloader.download(mangas)

    def test_download_chapter(self):
        mangas = {
            "chapter": {
                "url": "https://www.japscan.co/lecture-en-ligne/shingeki-no-kyojin/116/"
            }
        }

        self.japscandownloader.download(mangas)

    def test_download_chapters(self):
        chapters = {
            "chapters": {
                "url": "https://www.japscan.co/lecture-en-ligne/black-clover/",
                "chapter_min": 158,
                "chapter_max": 161,
            }
        }

        self.japscandownloader.download(chapters)

    def tearDown(self):
        if os.path.exists(self.japscandownloader.destination_path):
            shutil.rmtree(self.japscandownloader.destination_path, ignore_errors=True)
