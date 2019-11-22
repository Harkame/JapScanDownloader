import sys, os

import unittest
import numpy
from ..helpers import helper_scrambling
from bs4 import BeautifulSoup

from PIL import Image


class TestScrambling(unittest.TestCase):
    def test_unscramble_image(self):
        scrambled_image = os.path.join(
            ".", "tests", "test_scrambling", "test_scrambled_image.png"
        )
        unscrambled_image = os.path.join(
            ".", "tests", "test_scrambling", "test_unscrambled_image.png"
        )
        temp_unscrambled_image = os.path.join(
            ".", "tests", "test_scrambling", "test_temp_unscrambled_image.png"
        )

        helper_scrambling.unscramble_image(scrambled_image, temp_unscrambled_image)

        images = [None, None]
        for i, f in enumerate([unscrambled_image, temp_unscrambled_image]):
            images[i] = (
                numpy.array(
                    Image.open(f).convert("L").resize((32, 32), resample=Image.BICUBIC)
                )
            ).astype(
                numpy.int
            )  # convert from unsigned bytes to signed int using numpy
        self.assertEqual(numpy.abs(images[0] - images[1]).sum(), 0)

        # os.remove(temp_unscrambled_image

    def test_is_scrambled_scripts(self):
        page_url = os.path.join(
            ".", "tests", "test_scrambling", "test_scrambled_page.html"
        )

        page = BeautifulSoup(open(page_url, encoding="utf-8"), features="lxml")

        self.assertTrue(helper_scrambling.is_scrambled_scripts(page))

        page_url = os.path.join(
            ".", "tests", "test_scrambling", "test_not_scrambled_page.html"
        )

        page = BeautifulSoup(open(page_url, encoding="utf-8"), features="lxml")

        self.assertFalse(helper_scrambling.is_scrambled_scripts(page))

    def test_is_scrambled_clel(self):
        self.assertFalse(
            helper_scrambling.is_scrambled_clel(
                "https://www.japscan.to/lecture-en-ligne/shingeki-no-kyojin/114/2.html"
            )
        )
        self.assertTrue(
            helper_scrambling.is_scrambled_clel(
                "https://www.japscan.to/lecture-en-ligne/clel/shingeki-no-kyojin/114/2.html"
            )
        )
