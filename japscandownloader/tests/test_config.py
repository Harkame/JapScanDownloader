import sys, os

from ..helpers import get_config

import unittest


class ConfigTest(unittest.TestCase):
    def test_get_config(self):
        config = get_config(
            os.path.join(os.path.dirname(__file__), "test_config", "test_config.yml")
        )
        self.assertEqual(config["destination_path"], "./mymangas/")
        self.assertEqual(config["manga_format"], "pdf")
        self.assertEqual(len(config["mangas"]), 2)
        self.assertEqual(
            config["mangas"][0]["url"],
            "https://www.japscan.to/manga/shingeki-no-kyojin/",
        )
        self.assertEqual(
            config["mangas"][1]["url"], "https://www.japscan.to/manga/hunter-x-hunter/"
        )
