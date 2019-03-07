import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import config.config as config #all global variables and constants

import unittest

class JapScanDownloaderTest(unittest.TestCase):
    def test_shuffle(self):
        print('TODO')

if __name__ == '__main__':
    unittest.main()
