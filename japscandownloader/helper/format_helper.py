from PIL import Image
import os

import zipfile #zip
from os.path import basename #basename

def create_pdf(path, pdf_file_name):
    images = []

    for file in os.listdir(path):
        if file.endswith('.jpg') or file.endswith('.png'):
            image = Image.open(os.path.join(path, file))
            images.append(image.convert("RGB"))

    images[0].save(pdf_file_name, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])


def create_cbz(path, cbz_file_name):
    zipf = zipfile.ZipFile(cbz_file_name, 'w', zipfile.ZIP_DEFLATED)

    for file in os.listdir(path):
        if file.endswith('.jpg') or file.endswith('.png'):
            zipf.write(os.path.join(path, file), basename(os.path.join(path, file)))

    zipf.close()

def delete_images(path):
    for file in os.listdir(path):
        if file.endswith('.jpg') or file.endswith('.png'):
            os.remove(os.path.join(path, file))
