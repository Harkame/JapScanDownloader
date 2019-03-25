import os.path, sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import helper.argument_helper as argument_helper
import helper.config_helper as config_helper
import helper.unscramble_helper as unscramble_helper
import helper.format_helper as format_helper
import helper.download_helper as download_helper

import settings.settings as settings

import cfscrape
import unittest
import numpy
from PIL import Image
import shutil

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
        self.assertEqual(config['destination_path'], './mymangas/')
        self.assertEqual(config['manga_format'], 'pdf')
        self.assertEqual(len(config['mangas']), 2)
        self.assertEqual(config['mangas'][0]['url'], 'https://www.japscan.to/manga/shingeki-no-kyojin/')
        self.assertEqual(config['mangas'][1]['url'], 'https://www.japscan.to/manga/hunter-x-hunter/')

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

        #os.remove(temp_unscrambled_image)

class FormatTest(unittest.TestCase):
    chapter = os.path.join('.', 'tests', 'test_chapter')
    file_name = None
    image_number = 10

    def setUp(self):
        dirname = os.path.join('.', 'tests', 'test_chapter')

        if not os.path.exists(dirname):
            os.makedirs(dirname)

        for image_index in range(0, self.image_number):
            image_array = numpy.random.rand(500, 500, 3) * 255
            image = Image.fromarray(image_array.astype('uint8')).convert('RGBA')
            image_name = os.path.join('.', 'tests', 'test_chapter', ('temp_%s.png' % (image_index)))
            image.save(image_name)

    def test_format_pdf(self):
        self.file_name = os.path.join('.', 'tests', 'test_chapter.pdf')

        format_helper.create_pdf(self.chapter, self.file_name)

        self.assertGreater(os.path.getsize(self.file_name), 0)

    def test_format_cbz(self):
        self.file_name = os.path.join('.', 'tests', 'test_chapter.cbz')

        format_helper.create_cbz(self.chapter, self.file_name)

        self.assertGreater(os.path.getsize(self.file_name), 0)

    def tearDown(self):
        format_helper.delete_images(self.chapter)

        os.remove(self.file_name)


class DeleteTest(unittest.TestCase):
    chapter = os.path.join('.', 'tests', 'test_chapter')
    image_number = 10

    def setUp(self):
        dirname = os.path.join('.', 'tests', 'test_chapter')

        if not os.path.exists(dirname):
            os.makedirs(dirname)

        for image_index in range(0, self.image_number):
            image_array = numpy.random.rand(500, 500, 3) * 255
            image = Image.fromarray(image_array.astype('uint8')).convert('RGBA')
            image_name = os.path.join('.', 'tests', 'test_chapter', ('temp_%s.png' % (image_index)))
            image.save(image_name)

    def test_delete_images(self):
        image_counter = 0

        for file in os.listdir(self.chapter):
            if file.endswith('.jpg') or file.endswith('.png'):
                image_counter += 1

        self.assertEqual(image_counter, self.image_number)

        format_helper.delete_images(self.chapter)

        image_counter = 0;

        for file in os.listdir(self.chapter):
            if file.endswith('.jpg') or file.endswith('.png'):
                image_counter += 1

        self.assertEqual(image_counter, 0)

class DownloadTest(unittest.TestCase):
    def setUp(self):
        settings.init()

        settings.manga_format = 'png'
        settings.destination_path = os.path.join('.', 'tests', 'test_download')

        if not os.path.exists(settings.destination_path):
            os.makedirs(settings.destination_path)

    def test_download_chapter(self):
        scraper = cfscrape.create_scraper()

        chapter_url = 'https://www.japscan.to/lecture-en-ligne/hajime-no-ippo/1255/'

        download_helper.download_chapter(scraper, chapter_url)

    def test_download_page(self):
        scraper = cfscrape.create_scraper()

        page_url = 'https://www.japscan.to/lecture-en-ligne/hajime-no-ippo/1255/1.html'

        download_helper.download_page(scraper, page_url)

    def tearDown(self):
        if os.path.exists(settings.destination_path):
            shutil.rmtree(settings.destination_path, ignore_errors=True)
