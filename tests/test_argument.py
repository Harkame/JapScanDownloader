import sys, os

my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../japscandownloader/')
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import unittest

from helpers import helper_argument

class TestArgument(unittest.TestCase):
    def test_short_option(self):
        arguments = helper_argument.get_arguments(['-v', '-c', './myconfig.yml', '-d', './mymangas', '-f', 'myformat', '-u', '-k', '-r'])

        self.assertEqual(arguments.verbose, 1)
        self.assertEqual(arguments.config_file, './myconfig.yml')
        self.assertEqual(arguments.destination_path, './mymangas')
        self.assertEqual(arguments.format, 'myformat')
        self.assertEqual(arguments.unscramble, 1)
        self.assertEqual(arguments.keep, 1)
        self.assertEqual(arguments.reverse, 1)

    def test_long_option(self):
        arguments = helper_argument.get_arguments(['--verbose', '--config_file', './myconfig.yml', '--destination_path', './mymangas', '--format', 'myformat', '--unscramble', '--keep', '--reverse'])

        self.assertEqual(arguments.verbose, 1)
        self.assertEqual(arguments.config_file, './myconfig.yml')
        self.assertEqual(arguments.destination_path, './mymangas')
        self.assertEqual(arguments.format, 'myformat')
        self.assertEqual(arguments.unscramble, 1)
        self.assertEqual(arguments.keep, 1)
        self.assertEqual(arguments.reverse, 1)

    def test_multiple_verbose(self):
        verbosity_argument = '-'

        for verbosity_level in range(1, 10):
            verbosity_argument += 'v'
            arguments = helper_argument.get_arguments([verbosity_argument])
            self.assertEqual(arguments.verbose, verbosity_level)
