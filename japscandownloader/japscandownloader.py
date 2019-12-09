import cloudscraper
import sys

import os
from os.path import basename
import logging

from bs4 import BeautifulSoup
import os
from tqdm import tqdm
from urllib.parse import urlparse

JAPSCAN_URL = "https://www.japscan.to"

logger = logging.getLogger(__name__)

from .helpers import (
    get_arguments,
    get_config,
    create_pdf,
    create_cbz,
    unscramble_image,
    is_scrambled_scripts,
    is_scrambled_clel,
)


DEFAULT_CONFIG_FILE = os.path.join(".", "config.yml")
DEFAULT_DESTINATION_PATH = os.path.join(".", "mangas")
DEFAULT_format = "jpg"


class JapScanDownloader:
    def __init__(self, scraper):
        self.scraper = scraper

        self.config_file = DEFAULT_CONFIG_FILE
        self.destination_path = DEFAULT_DESTINATION_PATH
        self.keep = False
        self.reverse = False
        self.format = DEFAULT_format
        self.unscramble = False
        self.mangas = []

    def init(self, arguments):
        self.init_arguments(arguments)

        self.init_config()

        logger.debug("config_file : %s", self.config_file)
        logger.debug("destination_path : %s", self.destination_path)
        logger.debug("keep : %s", self.keep)
        logger.debug("reverse : %s", self.reverse)
        logger.debug("format : %s", self.format)
        logger.debug("unscramble : %s", self.unscramble)
        logger.debug("mangas : %s", self.mangas)

    def init_arguments(self, arguments):
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
            self.config_file = arguments.config_file

        if arguments.destination_path:
            self.destination_path = arguments.destination_path

        if arguments.format:
            self.format = arguments.format

        if arguments.reverse:
            self.reverse = True

        if arguments.keep:
            self.keep = True

        if arguments.unscramble:
            self.unscramble = True

    def init_config(self):
        config = get_config(self.config_file)

        if self.mangas is not None:
            self.mangas.extend(config["mangas"])

        if (
            self.destination_path == DEFAULT_DESTINATION_PATH
            and self.destination_path is not None
        ):
            self.destination_path = config["destination_path"]

        if self.format == DEFAULT_format and self.format is not None:
            self.format = config["format"]

    def download(self, manga):
        print(manga)
        if "url" in manga:
            manga_page = BeautifulSoup(
                self.scraper.get(manga["url"]).content, features="lxml"
            )

            chapter_divs = manga_page.findAll(
                "div", {"class": "chapters_list text-truncate"}
            )

            chapters_progress_bar = tqdm(
                total=len(chapter_divs),
                position=0,
                bar_format="[{bar}] - [{n_fmt}/{total_fmt}] - [chapters]",
            )

            chapters = None

            if self.reverse:
                chapters = reversed(chapter_divs)
            else:
                chapters = chapter_divs

            for chapter_div in chapters:
                chapter_tag = chapter_div.find(href=True)

                chapter_name = (
                    chapter_tag.contents[0].replace("\t", "").replace("\n", "")
                )

                logger.debug("chapter_name : %s", chapter_name)

                chapter_url = JAPSCAN_URL + chapter_tag["href"]

                self.download_chapter(chapter_url)

            chapters_progress_bar.close()

        elif "chapters" in manga:
            base_counter = manga["chapter_min"]

            diff = (manga["chapter_max"] - manga["chapter_min"]) + 1  # included

            chapters_progress_bar = tqdm(
                total=diff,
                position=0,
                bar_format="[{bar}] - [{n_fmt}/{total_fmt}] - [chapters]",
            )

            while base_counter <= manga["chapter_max"]:
                self.download_chapter(
                    manga["chapters"]["url"] + str(base_counter) + "/"
                )
                base_counter += 1

            chapters_progress_bar.close()
        else:
            self.download_chapter(manga["chapter"])

    def download_chapter(self, chapter_url):
        logger.debug("chapter_url : %s", chapter_url)

        pages = BeautifulSoup(
            self.scraper.get(chapter_url).content, features="lxml"
        ).find("select", {"id": "pages"})

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

        chapter_path = os.path.join(self.destination_path, manga_name, chapter_number)

        image_files = []

        for page_tag in page_options:
            page_url = JAPSCAN_URL + page_tag["value"]

            logger.debug("page_url : %s", page_url)

            file = self.download_page(chapter_path, page_url)

            if file is not None:
                image_files.append(file)

            pages_progress_bar.update(1)

        pages_progress_bar.close()

        if self.format == "pdf":
            create_pdf(
                chapter_path,
                os.path.join(chapter_path, chapter_number + ".pdf"),
                image_files,
            )

        elif self.format == "cbz":
            create_cbz(
                chapter_path,
                os.path.join(chapter_path, chapter_number + ".cbz"),
                image_files,
            )

        if self.format != DEFAULT_format and not self.keep:
            for image_file in image_files:
                os.remove(image_file)

    def download_page(self, chapter_path, page_url):
        logger.debug("page_url: %s", page_url)

        page = BeautifulSoup(self.scraper.get(page_url).content, features="lxml")

        image_url = page.find("div", {"id": "image"})["data-src"]

        response = self.scraper.get(image_url)

        if response.status_code != 200:
            return

        unscramble = is_scrambled_scripts(page)

        if self.unscramble:
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
