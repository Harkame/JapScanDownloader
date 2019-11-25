import settings

import cloudscraper
import sys
from PIL import Image

import os
from os.path import basename
import zipfile
import logging

from bs4 import BeautifulSoup
import os
from tqdm import tqdm

from urllib.parse import urlparse
from yaml import Loader, load

import argparse

JAPSCAN_URL = "https://www.japscan.to"

logger = logging.getLogger()


DEFAULT_CONFIG_FILE = os.path.join(".", "config.yml")
DEFAULT_DESTINATION_PATH = os.path.join(".", "mangas")
DEFAULT_MANGA_FORMAT = "jpg"

logger = logging.getLogger()
config_file = None
destination_path = None
keep = False
manga_format = None
reverse = False
unscramble = False
mangas = []


def init(arguments):
    global logger

    global config_file
    global destination_path
    global keep
    global manga_format
    global reverse

    global mangas

    config_file = DEFAULT_CONFIG_FILE

    init_arguments(arguments)

    init_config()

    logger.debug("config_file : %s", config_file)
    logger.debug("destination_path : %s", destination_path)
    logger.debug("keep : %s", keep)
    logger.debug("manga_format : %s", manga_format)

    logger.debug("reverse : %s", reverse)

    logger.debug("mangas : %s", mangas)


def init_arguments(arguments):
    global logger

    global config_file
    global destination_path
    global keep
    global manga_format
    global reverse
    global unscramble

    global mangas

    arguments = get_arguments(arguments)

    if arguments.verbose:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s :: %(levelname)s :: %(module)s :: %(lineno)s :: %(funcName)s :: %(message)s"
        )
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        if arguments.verbose == 0:
            logger.setLevel(logging.NOTSET)
        elif arguments.verbose == 1:
            logger.setLevel(logging.DEBUG)
        elif arguments.verbose == 2:
            logger.setLevel(logging.INFO)
        elif arguments.verbose == 3:
            logger.setLevel(logging.WARNING)
        elif arguments.verbose == 4:
            logger.setLevel(logging.ERROR)
        elif arguments.verbose == 5:
            logger.setLevel(logging.CRITICAL)

        logger.addHandler(stream_handler)

    if arguments.config_file:
        config_file = arguments.config_file

    if arguments.destination_path:
        destination_path = arguments.destination_path

    if arguments.format:
        manga_format = arguments.format

    if arguments.reverse:
        reverse = True

    if arguments.keep:
        keep = True

    if arguments.unscramble:
        unscramble = True


def init_config():
    global logger

    global config_file
    global destination_path
    global keep
    global manga_format
    global reverse

    global mangas

    config = get_config(config_file)

    if config["mangas"] is not None:
        mangas.extend(config["mangas"])

    if destination_path is None:
        if config["destination_path"] is not None:
            destination_path = config["destination_path"]
        else:
            destination_path = DEFAULT_DESTINATION_PATH

    if manga_format is None:
        if config["manga_format"] is not None:
            manga_format = config["manga_format"]
        else:
            manga_format = DEFAULT_MANGA_FORMAT


def get_arguments(arguments):
    argument_parser = argparse.ArgumentParser(
        description="Script to download mangas from JapScan",
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999),
    )

    argument_parser.add_argument(
        "-c",
        "--config_file",
        help=f"Set config file"
        "{os.linesep}"
        "Example : python japscandownloader/main.py -c /home/myconfigfile.yml",
        type=str,
    )

    argument_parser.add_argument(
        "-d",
        "--destination_path",
        help=f"Set destination path of downloaded mangas"
        "Example : python japscandownloader/main.py -d /home/mymangas/",
        type=str,
    )

    argument_parser.add_argument(
        "-f",
        "--format",
        help=f"Set format of downloaded mangas"
        "Example : python japscandownloader/main.py -f cbz|pdf|jpg|png",
        type=str,
    )

    argument_parser.add_argument(
        "-v",
        "--verbose",
        help=f"Active verbose mode, support different level"
        "Example : python japscandownloader/main.py -vv",
        action="count",
    )

    argument_parser.add_argument(
        "-r",
        "--reverse",
        help=f"Reverse chapters download order"
        "Default : Last to first"
        "Example : python japscandownloader/main.py -r",
        action="count",
    )

    argument_parser.add_argument(
        "-k",
        "--keep",
        help=f"Keep downloaded images (when format is pdf/cbz)"
        "Default : false"
        "Example : python japscandownloader/main.py -k",
        action="count",
    )

    argument_parser.add_argument(
        "-u",
        "--unscramble",
        help="Force unscrambling" "Example : python japscandownloader/main.py -u",
        action="count",
    )

    return argument_parser.parse_args(arguments)


def download(scraper, manga):
    if "url" in manga:
        manga_page = BeautifulSoup(scraper.get(manga["url"]).content, features="lxml")

        chapter_divs = manga_page.findAll(
            "div", {"class": "chapters_list text-truncate"}
        )

        chapters_progress_bar = tqdm(
            total=len(chapter_divs),
            position=0,
            bar_format="[{bar}] - [{n_fmt}/{total_fmt}] - [chapters]",
        )

        chapters = None

        if reverse:
            chapters = reversed(chapter_divs)
        else:
            chapters = chapter_divs

        for chapter_div in chapters:
            chapter_tag = chapter_div.find(href=True)

            chapter_name = chapter_tag.contents[0].replace("\t", "").replace("\n", "")

            logger.debug("chapter_name : %s", chapter_name)

            chapter_url = JAPSCAN_URL + chapter_tag["href"]

            download_chapter(scraper, chapter_url)

        chapters_progress_bar.close()

    elif "chapters" in manga:
        base_counter = manga["chapters"]["chapter_min"]

        diff = (
            manga["chapters"]["chapter_max"] - manga["chapters"]["chapter_min"]
        ) + 1  # included

        chapters_progress_bar = tqdm(
            total=diff,
            position=0,
            bar_format="[{bar}] - [{n_fmt}/{total_fmt}] - [chapters]",
        )

        while base_counter <= manga["chapters"]["chapter_max"]:
            download_chapter(
                scraper, manga["chapters"]["url"] + str(base_counter) + "/"
            )
            base_counter += 1

        chapters_progress_bar.close()
    else:
        download_chapter(scraper, manga["chapter"])


def download_chapter(scraper, chapter_url):
    logger.debug("chapter_url : %s", chapter_url)

    pages = BeautifulSoup(scraper.get(chapter_url).content, features="lxml").find(
        "select", {"id": "pages"}
    )

    page_options = pages.findAll("option", value=True)

    pages_progress_bar = tqdm(
        total=len(page_options),
        position=1,
        bar_format="[{bar}] - [{n_fmt}/{total_fmt}] - [pages]",
    )

    data = chapter_url.split("/")

    logger.debug("data : %s", str(data))

    manga_name = data[4]
    chapter_number = data[5]

    chapter_path = os.path.join(destination_path, manga_name, chapter_number)

    image_files = []

    for page_tag in page_options:
        page_url = JAPSCAN_URL + page_tag["value"]

        logger.debug("page_url : %s", page_url)

        file = download_page(scraper, chapter_path, page_url)

        if file is not None:
            image_files.append(file)

        pages_progress_bar.update(1)

    pages_progress_bar.close()

    if manga_format == "pdf":
        create_pdf(
            chapter_path,
            os.path.join(chapter_path, chapter_number + ".pdf"),
            image_files,
        )
        if not keep:
            for image_file in image_files:
                os.remove(image_file)

    elif manga_format == "cbz":
        create_cbz(
            chapter_path,
            os.path.join(chapter_path, chapter_number + ".cbz"),
            image_files,
        )
        if not keep:
            for image_file in image_files:
                os.remove(image_file)


def download_page(scraper, chapter_path, page_url):
    logger.debug("page_url: %s", page_url)

    page = BeautifulSoup(scraper.get(page_url).content, features="lxml")

    image_url = page.find("div", {"id": "image"})["data-src"]

    response = scraper.get(image_url)

    if response.status_code != 200:
        return

    unscramble = is_scrambled_scripts(page)

    if unscramble:
        unscramble = True

    logger.debug("unscramble : %s", unscramble)

    logger.debug("image_url: %s", image_url)

    reverse_image_url = image_url[::-1]

    image_name = urlparse(image_url).path.split("/")[-1]

    image_full_path = os.path.join(chapter_path, image_name)

    logger.debug("image_full_path : %s", image_full_path)

    slash_counter = 0
    index = 0

    while slash_counter < 3:
        if reverse_image_url[index] == "/":
            slash_counter += 1
        index += 1

    reverse_image_url = reverse_image_url[0:index]

    image_path = reverse_image_url[::-1]

    logger.debug("image_path : %s", image_path)

    logger.debug("image_full_path : %s", image_full_path)

    if not os.path.exists(os.path.dirname(image_full_path)):
        try:
            os.makedirs(os.path.dirname(image_full_path))
            logger.debug("File created : %s", image_full_path)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    image_content = response.content

    unscramble = True

    if unscramble is True:
        scrambled_image = image_full_path + "_scrambled"
    else:
        scrambled_image = image_full_path

    file = open(scrambled_image, "wb")

    file.write(image_content)

    file.close()

    if unscramble is True:
        unscramble_image(scrambled_image, image_full_path)
        os.remove(scrambled_image)

    return image_full_path


def get_config(config_file_path):
    config_file = open(config_file_path, "r")

    config = load(config_file, Loader=Loader)

    config_file.close()

    return config


def unscramble_image(scrambled_image, image_full_path):
    input_image = Image.open(scrambled_image)
    temp = Image.new("RGB", input_image.size)
    output_image = Image.new("RGB", input_image.size)
    for x in range(0, input_image.width, 200):
        col1 = input_image.crop((x, 0, x + 100, input_image.height))
        if (x + 200) <= input_image.width:
            col2 = input_image.crop((x + 100, 0, x + 200, input_image.height))
            temp.paste(col1, (x + 100, 0))
            temp.paste(col2, (x, 0))
        else:
            col2 = input_image.crop((x + 100, 0, input_image.width, input_image.height))
            temp.paste(col1, (x, 0))
            temp.paste(col2, (x + 100, 0))
    for y in range(0, temp.height, 200):
        row1 = temp.crop((0, y, temp.width, y + 100))
        if (y + 200) <= temp.height:
            row2 = temp.crop((0, y + 100, temp.width, y + 200))
            output_image.paste(row1, (0, y + 100))
            output_image.paste(row2, (0, y))
        else:
            row2 = temp.crop((0, y + 100, temp.width, temp.height))
            output_image.paste(row1, (0, y))
            output_image.paste(row2, (0, y + 100))
    output_image.save(image_full_path)


def is_scrambled_scripts(page):
    scripts = page.find("head").find_all("script")

    if len(scripts) > 9:
        script = scripts[8]

        logger.debug("script : %s", script)

        if "_" in str(script):
            logger.debug("scrambled image")
            return True

    return False


# Old way to detect scrambling
def is_scrambled_clel(image_url):
    if "clel" in image_url:
        logger.debug("scrambled image")
        return True

    return False


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


def main(arguments):
    init(arguments)

    scraper = cloudscraper.create_scraper()

    html = scraper.get("https://www.japscan.co/")

    for manga in mangas:
        download(scraper, manga)


if __name__ == "__main__":
    main(sys.argv[1:])
