import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import helper.argument_helper as argument_helper
import helper.config_helper as config_helper

import helper.unscramble_helper as unscramble_helper

import unittest

class ArgumentTest(unittest.TestCase):
    def test_short_option(self):
        arguments = argument_helper.get_arguments(['-v', '-c', './myconfig.yml', '-d', './mymangas', '-f', 'myformat'])

        self.assertEqual(arguments.verbose, 1)
        self.assertEqual(arguments.config_file, './myconfig.yml')
        self.assertEqual(arguments.destination_path, './mymangas')
        self.assertEqual(arguments.format, 'myformat')

    def test_long_option(self):
        arguments = argument_helper.get_arguments(['--verbose', '--config_file', './myconfig.yml', '--destination_path', './mymangas', '--format', 'myformat'])

        self.assertEqual(arguments.verbose, 1)
        self.assertEqual(arguments.config_file, './myconfig.yml')
        self.assertEqual(arguments.destination_path, './mymangas')
        self.assertEqual(arguments.format, 'myformat')

    def test_multiple_verbose(self):
        verbosity_argument = '-'

        for verbosity_level in range(1, 10):
            verbosity_argument += 'v'
            arguments = argument_helper.get_arguments([verbosity_argument])
            self.assertEqual(arguments.verbose, verbosity_level)

class ConfigTest(unittest.TestCase):
    def test_get_config(self):
        config = config_helper.get_config(os.path.join('.', 'tests', 'test_config.yml'))
        self.assertEqual(config['destinationPath'], './mymangas/')
        self.assertEqual(config['mangaFormat'], 'pdf')
        self.assertEqual(len(config['mangas']), 2)
        self.assertEqual(config['mangas'][0]['url'], 'https://www.japscan.to/manga/shingeki-no-kyojin/')
        self.assertEqual(config['mangas'][1]['url'], 'https://www.japscan.to/manga/hunter-x-hunter/')

#TODO

class UnscrambleTest(unittest.TestCase):
    def test_unscramble_image(self):
        print('todo')

class FormatTest(unittest.TestCase):
    def test_format_pdf(self):
        print('todo')

    def test_format_cbz(self):
        print('todo')

class DownloadTest(unittest.TestCase):
    def test_download(self):
        print('todo')
