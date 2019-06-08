import sys, os

my_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, my_path + '/../japscandownloader/')
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import unittest

import numpy
from PIL import Image

from helpers import helper_format

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

        helper_format.delete_images(self.chapter)

        image_counter = 0;

        for file in os.listdir(self.chapter):
            if file.endswith('.jpg') or file.endswith('.png'):
                image_counter += 1

        self.assertEqual(image_counter, 0)
