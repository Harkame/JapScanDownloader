import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import helper.argument_helper as argument_helper
import helper.config_helper as config_helper
import helper.unscramble_helper as unscramble_helper
import helper.format_helper as format_helper

import unittest

import numpy

from PIL import Image

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
        config = config_helper.get_config(os.path.join('.', 'tests', 'test_config', 'test_config.yml'))
        self.assertEqual(config['destinationPath'], './mymangas/')
        self.assertEqual(config['mangaFormat'], 'pdf')
        self.assertEqual(len(config['mangas']), 2)
        self.assertEqual(config['mangas'][0]['url'], 'https://www.japscan.to/manga/shingeki-no-kyojin/')
        self.assertEqual(config['mangas'][1]['url'], 'https://www.japscan.to/manga/hunter-x-hunter/')
#TODO

class UnscrambleTest(unittest.TestCase):
    def test_unscramble_image(self):
        scrambled_image = os.path.join('.', 'tests', 'test_unscramble', 'test_scrambled_image.png')
        unscrambled_image = os.path.join('.', 'tests', 'test_unscramble', 'test_unscrambled_image.png')
        temp_unscrambled_image = os.path.join('.', 'tests', 'test_unscramble', 'test_temp_unscrambled_image.png')

        unscramble_helper.unscramble_image(scrambled_image, temp_unscrambled_image);

        images = [None, None]
        for i, f in enumerate([unscrambled_image, temp_unscrambled_image]):
            images[i] = (numpy.array(Image.open(f).convert('L').resize((32,32), resample=Image.BICUBIC))).astype(numpy.int)   # convert from unsigned bytes to signed int using numpy
        self.assertEqual(numpy.abs(images[0] - images[1]).sum(), 0)

        os.remove(temp_unscrambled_image)

class FormatTest(unittest.TestCase):
    def setUp(self):
        for image_index in range(0, 10):
            image_array = numpy.random.rand(500, 500, 3) * 255
            image = Image.fromarray(image_array.astype('uint8')).convert('RGBA')
            image.save(os.path.join('.', 'tests', 'test_chapter', ('temp_%s.png' % (image_index))))

    def test_format_pdf(self):
        chapter = os.path.join('.', 'tests', 'test_chapter')
        file_name = os.path.join('.', 'tests', 'test_chapter.pdf')

        format_helper.create_pdf(chapter, file_name)

        format_helper.delete_images(chapter)

        os.remove(file_name)

    def test_format_cbz(self):
        chapter = os.path.join('.', 'tests', 'test_chapter')
        file_name = os.path.join('.', 'tests', 'test_chapter.cbz')

        format_helper.create_cbz(chapter, file_name)

        format_helper.delete_images(chapter)

        os.remove(file_name)

class DownloadTest(unittest.TestCase):
    def test_download(self):
        print('todo')
