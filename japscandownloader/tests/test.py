import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from unscramble.unscramble import unscramble_image #unscramble method

from manga_format.manga_format_cbz import create_cbz #manga format cbz archive
from manga_format.manga_format_pdf import create_pdf #manga format pdf

import config.config as config #all global variables and constants

from helper.config_helper import get_config #helper config
from helper.argument_helper import get_arguments #helper arguments

import unittest

class RandomTest(unittest.TestCase):
    def test_shuffle(self):
        print('TODO')

if __name__ == '__main__':
    unittest.main()
