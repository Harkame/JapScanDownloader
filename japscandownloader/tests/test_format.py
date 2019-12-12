import os

import unittest

from ..helpers import create_cbz, create_pdf

import numpy
from PIL import Image


class TestFormat(unittest.TestCase):
    chapter = os.path.join(os.path.dirname(__file__), "test_chapter")
    image_number = 10

    def setUp(self):
        self.image_files = []

        if not os.path.exists(self.chapter):
            os.makedirs(self.chapter)

        for image_index in range(0, self.image_number):
            image_array = numpy.random.rand(500, 500, 3) * 255
            image = Image.fromarray(image_array.astype("uint8")).convert("RGBA")
            image_full_path = os.path.join(
                os.path.dirname(__file__),
                "test_chapter",
                ("temp_%s.png" % (image_index)),
            )
            self.image_files.append(image_full_path)
            image.save(image_full_path)

    def test_format_pdf(self):
        self.file_name = os.path.join(
            os.path.dirname(__file__), "test_chapter", "test_chapter.pdf"
        )

        create_pdf(self.chapter, self.file_name, self.image_files)

        self.assertGreater(os.path.getsize(self.file_name), 0)

    def test_format_cbz(self):
        self.file_name = os.path.join(
            os.path.dirname(__file__), "test_chapter", "test_chapter.cbz"
        )

        create_cbz(self.chapter, self.file_name, self.image_files)

        self.assertGreater(os.path.getsize(self.file_name), 0)

    def tearDown(self):
        for image_file in self.image_files:
            os.remove(image_file)

        os.remove(self.file_name)
