from PIL import Image
import glob
import logging #logs
import os


def create_pdf(path, file_name):
    images = []
    images_name = []

    for image_name in glob.glob(path + '*.png'):
        image = Image.open(image_name)
        images.append(image.convert("RGB"))
        images_name.append(image_name)

    images[0].save(file_name, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])

    for image_name in images_name:
        os.remove(image_name)
