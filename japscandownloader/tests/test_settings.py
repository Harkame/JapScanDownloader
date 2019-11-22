import sys, os

from ..settings import settings

import unittest


class SettingsTest(unittest.TestCase):
    def test_settings_init_arguments(self):
        settings.init_arguments("")

    def test_settings_init_config(self):
        # settings.init_config()
        pass
