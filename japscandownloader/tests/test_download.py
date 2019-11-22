'''
import os
import sys

my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../japscandownloader/')
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import unittest
import cloudscraper

from helpers import helper_download

from settings import settings

import shutil

class DownloadTests(unittest.TestCase):
    scraper = cloudscraper.create_scraper()

    def setUp(self):
        settings.manga_format = 'png'
        settings.destination_path = os.path.join('.', 'tests', 'test_download')

        if not os.path.exists(settings.destination_path):
            os.makedirs(settings.destination_path)

    def test_download_page(self):
        page_url = 'https://www.japscan.to/lecture-en-ligne/hajime-no-ippo/1255/1.html'

        chapter_path = os.path.join(settings.destination_path, 'hajime-no-ippo', '1255')

    def test_download_chapter(self):
        pass

        #chapter_url = 'https://www.japscan.to/lecture-en-ligne/hajime-no-ippo/1255/'

        #helper_download.download_chapter(self.scraper, chapter_url)

    def tearDown(self):
        if os.path.exists(settings.destination_path):
            shutil.rmtree(settings.destination_path, ignore_errors=True)
'''
