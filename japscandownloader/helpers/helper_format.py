import zipfile
import logging
from PIL import Image

logger = logging.getLogger(__name__)


def create_pdf(path, pdf_file_name, image_files):
    images = []

    for image_file in image_files:
        image = Image.open(image_file)
        images.append(image.convert("RGB"))

    images[0].save(
        pdf_file_name, "PDF", resolution=100.0, save_all=True, append_images=images[1:]
    )


def create_cbz(path, cbz_file_name, image_files):
    zipf = zipfile.ZipFile(cbz_file_name, "w", zipfile.ZIP_DEFLATED)

    for image_file in image_files:
        zipf.write(image_file, basename(image_file))

    zipf.close()
