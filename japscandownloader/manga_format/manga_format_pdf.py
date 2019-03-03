from PIL import Image #image
import glob #list image
import logging #logs
import os #remove=

def create_pdf(path, pdf_file_name):
    logging.debug('path : %s', path)
    logging.debug('pdf_file_name : %s', pdf_file_name)

    images = []

    for file in os.listdir(path):
        logging.debug('file : %s', file)
        if file.endswith('.png'):
            image = Image.open(os.path.join(path, file))
            images.append(image.convert("RGB"))
            os.remove(os.path.join(path, file))

    images[0].save(pdf_file_name, "PDF" ,resolution=100.0, save_all=True, append_images=images[1:])
