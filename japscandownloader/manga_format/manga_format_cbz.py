import logging #logs
import os #remove
import zipfile #zip
from os.path import basename #basename

def create_cbz(path, cbz_file_name):
    logging.debug('path : %s', path)
    logging.debug('cbz_file_name : %s', cbz_file_name)

    zipf = zipfile.ZipFile(cbz_file_name, 'w', zipfile.ZIP_DEFLATED)

    for file in os.listdir(path):
        logging.debug('file : %s', file)
        if file.endswith('.png'):
            zipf.write(os.path.join(path, file), basename(os.path.join(path, file)))
            os.remove(os.path.join(path, file))

    zipf.close()
