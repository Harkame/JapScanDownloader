from PIL import Image #image
import os #remove

import config.config as config #all global variables and constants

def create_pdf(path, pdf_file_name):
    images = []

    for file in os.listdir(path):
        if file.endswith('.jpg') or file.endswith('.png'):
            image = Image.open(os.path.join(path, file))
            images.append(image.convert("RGB"))
            os.remove(os.path.join(path, file))

    images[0].save(pdf_file_name, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])
