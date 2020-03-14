import logging

from bs4 import BeautifulSoup
import os
from tqdm import tqdm
from urllib.parse import urlparse
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import sys

JAPSCAN_URL = "https://www.japscan.to"

logger = logging.getLogger(__name__)


def process_browser_log_entry(entry):
    response = json.loads(entry["message"])["message"]
    return response


if __package__ is None or __package__ == "":
    from helpers import (
        get_arguments,
        get_config,
        create_pdf,
        create_cbz,
        unscramble_image,
        is_scrambled_scripts,
        process_browser_log_entry,
    )
else:
    from .helpers import (
        get_arguments,
        get_config,
        create_pdf,
        create_cbz,
        unscramble_image,
        is_scrambled_scripts,
        process_browser_log_entry,
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
        self.driver = None

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

        options = webdriver.ChromeOptions()
        options.add_argument("--user-data-dir=/home/username/.config/google-chrome")
        options.add_argument("--log-level=3")
        caps = DesiredCapabilities.CHROME
        caps["goog:loggingPrefs"] = {"performance": "ALL"}

        self.driver = webdriver.Chrome(
            self.driver_path, options=options, desired_capabilities=caps
        )

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

        if arguments.driver:
            self.driver_path = arguments.driver

    def init_config(self):
        config = get_config(self.config_file)

        if self.mangas is not None:
            self.mangas.extend(config["mangas"])

        if self.destination_path == DEFAULT_DESTINATION_PATH:
            self.destination_path = config["destination_path"]

        if self.format == DEFAULT_format:
            self.format = config["format"]

    def run(self, manga_url):
        self.driver.get(manga_url["url"])

        time.sleep(2)

        browser_log = self.driver.get_log("performance")
        events = [process_browser_log_entry(entry) for entry in browser_log]

        for event in events:
            if "params" in event:
                params = event["params"]
                if "response" in params:
                    response = params["response"]
                    if "url" in response:
                        url = response["url"]

                        if len(url) > 100:
                            print(event)
                            print(url)

        time.sleep(1000)

    def download(self, item):
        if "chapters" in item:
            chapters = item["chapters"]

            url = chapters["manga"]

            base_counter = chapters["min"]

            min = chapters["min"]
            max = chapters["max"]

            diff = (max - min) + 1  # included

            chapters_progress_bar = tqdm(
                total=diff,
                position=0,
                bar_format="[{bar}] - [{n_fmt}/{total_fmt}] - [chapters]",
            )

            while base_counter <= max:
                self.download_chapter(url + str(base_counter) + "/")
                base_counter += 1

            chapters_progress_bar.close()

        elif "chapter" in item:
            chapter = item["chapter"]

            self.download_chapter(chapter)
        elif "manga" in item:
            url = item["manga"]

            self.driver.get(url)

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div#main"))
            )

            chapters = []

            for chapter_tag in self.driver.find_elements_by_css_selector(
                "div.chapters_list.text-truncate a"
            ):
                chapter = {}
                chapter["url"] = chapter_tag.get_attribute("href")
                chapter["name"] = chapter_tag.text.replace("\t", "").replace("\n", "")

                chapters.append(chapter)

            chapters_progress_bar = tqdm(
                total=len(chapters),
                position=0,
                bar_format="[{bar}] - [{n_fmt}/{total_fmt}] - [chapters]",
            )

            for chapter in chapters:
                logger.debug("chapter_name : %s", chapter["name"])

                self.download_chapter(chapter["url"])

            chapters_progress_bar.close()

    def download_chapter(self, chapter_url):
        self.driver.get(chapter_url)

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "h1.text-center.mt-2.font-weight-bold")
            )
        )

        logger.debug("chapter_url : %s", chapter_url)

        pages = self.driver.find_element_by_css_selector("select#pages")

        if pages is None:
            raise Exception(f"Can't read pages {str(html)}")

        page_options = []

        for page_options_tag in pages.find_elements_by_css_selector("option"):
            print(page_options_tag.get_attribute("value"))
            page_options.append(page_options_tag.get_attribute("value"))

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

        for index, page_tag in enumerate(page_options):
            page_url = JAPSCAN_URL + page_tag

            logger.debug("page_url : %s", page_url)

            file = self.download_page(chapter_path, page_url, index)

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

    def download_page(self, chapter_path, page_url, index):
        logger.debug("page_url: %s", page_url)

        browser_log = self.driver.get_log("performance")
        events = [process_browser_log_entry(entry) for entry in browser_log]

        image_url = None

        for event in events:
            if "params" in event:
                params = event["params"]
                if "response" in params:
                    response = params["response"]
                    if "url" in response:
                        url = response["url"]

                        if len(url) > 100:
                            print(url)
                            image_url = url
                            break

        self.driver.get(page_url)

        unscramble = False

        logger.debug("unscramble : %s", unscramble)

        logger.debug("image_url: %s", image_url)

        if image_url is None:
            return

        logger.debug("image_url : %s", image_url)

        reverse_image_url = image_url[::-1]

        image_name = str(index) + ".jpg"

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

        response = self.scraper.get(image_url)

        if not os.path.exists(os.path.dirname(image_full_path)):
            try:
                os.makedirs(os.path.dirname(image_full_path))
                logger.debug("File created : %s", image_full_path)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

        image_content = response.content

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
