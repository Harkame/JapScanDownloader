import sys, os

my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../japscandownloader/')
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from settings import settings

import unittest

class SettingsTest(unittest.TestCase):
    def test_settings_init_arguments(self):
        settings.init_arguments('')

    def test_settings_init_config(self):
        #settings.init_config()
        pass
