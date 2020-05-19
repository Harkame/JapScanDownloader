import os
import shutil
import tempfile
import unittest

import cloudscraper
from japscandownloader.jss import JapScanDownloader

from .utils import network_required


class TestDownload(unittest.TestCase):
    scrapper = JapScanDownloader(cloudscraper.create_scraper())

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

        download_path = os.path.join(self.test_dir, "test_download")
        os.makedirs(download_path, exist_ok=True)

        self.scrapper.destination_path = download_path

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    @network_required
    def test_download_manga(self):
        self.scrapper.download({
            "url": "https://www.japscan.co/manga/raba-the-mules/",
        })

    @network_required
    def test_download_chapter(self):
        self.scrapper.download({
            "chapter": {
                "url": "https://www.japscan.co/lecture-en-ligne/shingeki-no-kyojin/116/"
            }
        })

    @network_required
    def test_download_chapters(self):
        self.scrapper.download({
            "chapters": {
                "url": "https://www.japscan.co/lecture-en-ligne/black-clover/",
                "chapter_min": 158,
                "chapter_max": 161,
            }
        })
