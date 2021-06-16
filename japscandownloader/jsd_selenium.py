import errno
import logging
import math

import os
import shutil
from tqdm import tqdm
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import urllib3.exceptions
from random import randint

from PIL import Image
from io import BytesIO
import sys

from .helpers import (
    get_arguments,
    get_config,
    create_pdf,
    create_cbz,
    process_browser_log_entry,
)

JAPSCAN_URL = "https://www.japscan.to"

logger = logging.getLogger(__name__)


def process_browser_log_entry(entry):
    response = json.loads(entry["message"])["message"]
    return response


DEFAULT_CONFIG_FILE = os.path.join(".", "config.yml")
DEFAULT_DESTINATION_PATH = os.path.join(".", "mangas")
DEFAULT_format = "jpg"


class JapScanDownloader:
    def __init__(self):
        self.config_file = DEFAULT_CONFIG_FILE
        self.destination_path = DEFAULT_DESTINATION_PATH
        self.keep = False
        self.reverse = False
        self.format = DEFAULT_format
        self.mangas = []
        self.driver = None
        self.profile = None
        self.show = False

    def init(self, arguments):
        self.init_arguments(arguments)

        self.init_config()

        logger.debug("config_file : %s", self.config_file)
        logger.debug("destination_path : %s", self.destination_path)
        logger.debug("keep : %s", self.keep)
        logger.debug("reverse : %s", self.reverse)
        logger.debug("format : %s", self.format)
        logger.debug("mangas : %s", self.mangas)
        logger.debug("profile : %s", self.profile)
        logger.debug("show : %s", self.show)

        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_argument("window-size=1080,1920")
        options.add_argument("--profile-directory=Default")

        if self.profile is not None:
            options.add_argument(f"user-data-dir={self.profile}")

        options.add_argument("window-size=1440,2560")
        if not self.show:
            options.add_argument("--headless")

        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])

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

        if arguments.driver:
            self.driver_path = arguments.driver

        if arguments.profile:
            self.profile = arguments.profile

        if arguments.show:
            self.show = True

    def init_config(self):
        config = get_config(self.config_file)

        if self.mangas is not None:
            self.mangas.extend(config["mangas"])

        if self.destination_path == DEFAULT_DESTINATION_PATH:
            self.destination_path = config["destination_path"]

        if self.format == DEFAULT_format:
            self.format = config["format"]

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
                chapters_progress_bar.update(1)

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
                chapters_progress_bar.update(1)

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
            raise Exception(f"Can't read pages {str(chapter_url)}")

        page_options = []

        for page_options_tag in pages.find_elements_by_css_selector("option"):
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

            file = self.download_page(chapter_path, page_url, index, len(page_options))

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

    def prepend_zeroes(self, current_image_idx, total_images):
        """
        :param current_image_idx: Int value of current page number. Example : 1, 2, 3
        :param total_images: Total number of images in the chapter
        :return:
        """
        max_digits = int(math.log10(int(total_images))) + 1
        return str(current_image_idx).zfill(max_digits)

    def download_page(self, chapter_path, page_url, index, total):

        image_name = self.prepend_zeroes(index, total) + ".png"
        image_full_path = os.path.join(chapter_path, image_name)

        logger.debug("image_full_path : %s", image_full_path)

        if os.path.exists(image_full_path):
            logger.debug(f"skipping file : {image_full_path}")
            return image_full_path

        time.sleep(randint(1, 5))

        logger.debug(f"page_url : {page_url}")

        success = False

        while success is False:
            try:
                self.driver.get(page_url)
                success = True
            except urllib3.exceptions.ProtocolError:
                logger.debug(f"error self.driver.get({page_url}) retry")
                success = False
                time.sleep(5)

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

                        if len(url) > 130 and (
                            url.endswith(".jpg") or url.endswith(".png")
                        ):
                            image_url = url
                            break

        logger.debug("image_url: %s", image_url)

        # if image_url is None:
        #     return

        # reverse_image_url = image_url[::-1]
        #
        # slash_counter = 0
        # index = 0
        #
        # while slash_counter < 3:
        #     if reverse_image_url[index] == "/":
        #         slash_counter += 1
        #     index += 1
        #
        # reverse_image_url = reverse_image_url[0:index]
        #
        # image_path = reverse_image_url[::-1]
        #
        # logger.debug("image_path : %s", image_path)

        if not os.path.exists(os.path.dirname(image_full_path)):
            try:
                os.makedirs(os.path.dirname(image_full_path))
                logger.debug("File created : %s", image_full_path)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

        image_element = self.driver.find_element_by_id("image")

        im = None

        try:
            im = Image.open(BytesIO(image_element.screenshot_as_png))
        except Exception:  # Fail on get image
            logger.debug(f"error : invalid image_element.screenshot_as_png")
            time.sleep(4)

            try:  # Retry to get image after a fail
                im = Image.open(BytesIO(image_element.screenshot_as_png))
            except Exception:
                logger.debug(f"error retry : invalid image_element.screenshot_as_png")

        if im is not None:
            im.save(image_full_path)

        return image_full_path
