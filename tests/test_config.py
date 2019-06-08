import sys, os

my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../japscandownloader/')
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from helpers import helper_config

import unittest

class ConfigTest(unittest.TestCase):
    def test_get_config(self):
        config = helper_config.get_config(os.path.join('.', 'tests', 'test_config', 'test_config.yml'))
        self.assertEqual(config['destination_path'], './mymangas/')
        self.assertEqual(config['manga_format'], 'pdf')
        self.assertEqual(len(config['mangas']), 2)
        self.assertEqual(config['mangas'][0]['url'], 'https://www.japscan.to/manga/shingeki-no-kyojin/')
        self.assertEqual(config['mangas'][1]['url'], 'https://www.japscan.to/manga/hunter-x-hunter/')
