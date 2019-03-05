import os #remove
import zipfile #zip
from os.path import basename #basename

def create_cbz(path, cbz_file_name):
    zipf = zipfile.ZipFile(cbz_file_name, 'w', zipfile.ZIP_DEFLATED)

    for file in os.listdir(path):
        if file.endswith('.png'):
            zipf.write(os.path.join(path, file), basename(os.path.join(path, file)))
            os.remove(os.path.join(path, file))

    zipf.close()
