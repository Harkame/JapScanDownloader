import errno
import logging
import math
import os
import time
from io import BytesIO

import urllib3.exceptions
from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from tqdm import tqdm

from .helpers import (
    get_arguments,
    get_config,
    update_config,
    create_pdf,
    create_cbz,
)

JAPSCAN_URL = "https://www.japscan.to"

logger = logging.getLogger(__name__)

DEFAULT_CONFIG_FILE = os.path.join(".", "config.yml")
DEFAULT_DESTINATION_PATH = os.path.join(".", "mangas")
DEFAULT_format = "jpg"


class JapScanDownloader:
    def __init__(self):
        self.driver_path = None
        self.config_file = DEFAULT_CONFIG_FILE
        self.destination_path = DEFAULT_DESTINATION_PATH
        self.keep = False
        self.reverse = False
        self.format = DEFAULT_format
        self.mangas = []
        self.driver = None
        self.profile = None
        self.show = False
        self.split = False
        self.split_reverse = False
        self.retries = False

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
        logger.debug("split : %s", self.split)
        logger.debug("split_reverse : %s", self.split_reverse)

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

        if arguments.split:
            self.split = True
            self.split_reverse = True if arguments.split > 1 else False

        if arguments.retries:
            self.retries = True

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

            min_chapter = chapters["min"]
            max_chapter = chapters["max"]

            diff = (max_chapter - min_chapter) + 1  # included

            chapters_progress_bar = tqdm(
                total=diff,
                position=0,
                bar_format="[{bar}] - [{n_fmt}/{total_fmt}] - [chapters: " + url + "]",
            )

            while base_counter <= max_chapter:
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
                ec.presence_of_element_located((By.CSS_SELECTOR, "div#main"))
            )

            chapters = []

            for chapter_tag in self.driver.find_elements_by_css_selector(
                    "div.chapters_list.text-truncate a"
            ):
                chapter = {
                    "url": chapter_tag.get_attribute("href"),
                    "name": chapter_tag.text.replace("\t", "").replace("\n", "")
                }

                chapters.append(chapter)

            chapters_progress_bar = tqdm(
                total=len(chapters),
                position=0,
                bar_format="[{bar}] - [{n_fmt}/{total_fmt}] - [chapters: " + url + "]",
            )

            for chapter in chapters:
                logger.debug("chapter_name : %s", chapter["name"])

                self.download_chapter(chapter["url"])
                chapters_progress_bar.update(1)

            chapters_progress_bar.close()
        elif "subscription" in item:
            subscription = item["subscription"]
            url = subscription["manga"]
            previous_last_chapter = subscription["last_chapter"]

            self.driver.get(url)

            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located((By.CSS_SELECTOR, "div#main"))
            )

            chapters = []

            last_chapter = None

            for chapter_tag in self.driver.find_elements_by_css_selector(
                    "div.chapters_list.text-truncate a"
            ):
                skip_chapter = False
                badges = chapter_tag.find_elements_by_css_selector("span.badge")
                for badge in badges:
                    if "spoiler" in badge.text.lower():  # raw spoiler chapter not translated yet, skip download
                        skip_chapter = True
                        break
                    if "raw" in badge.text.lower():  # raw spoiler chapter not translated yet, skip download
                        skip_chapter = True
                        break

                if skip_chapter:
                    continue

                chapter = {
                    "url": chapter_tag.get_attribute("href"),
                    "name": chapter_tag.text.replace("\t", "").replace("\n", "")
                }

                if last_chapter is None:
                    last_chapter = chapter["url"]

                if chapter["url"] == previous_last_chapter:
                    break

                chapters.append(chapter)

            chapters_progress_bar = tqdm(
                total=len(chapters),
                position=0,
                bar_format="[{bar}] - [{n_fmt}/{total_fmt}] - [subscription: " + url + "]",
            )

            for chapter in reversed(chapters):
                logger.debug("chapter_name : %s", chapter["name"])
                self.download_chapter(chapter["url"])
                update_config(self.config_file, url, chapter["url"])
                chapters_progress_bar.update(1)

            chapters_progress_bar.close()

    def download_chapter(self, chapter_url):
        self.driver.get(chapter_url)

        WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located(
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
            page_number = (int(page_tag) + 1)
            page_url = chapter_url + str(page_number) + ".html"

            file = self.download_page(chapter_path, page_url, index, len(page_options))

            if file is not None:
                image_files.append(file)

                if self.split:
                    pic = Image.open(file)
                    if pic.size[1] / pic.size[0] < 0.9:
                        logger.debug("Split double page")

                        file_a = file[:-4] + "A" + file[-4:]
                        file_b = file[:-4] + "B" + file[-4:]

                        image_files.pop()
                        image_files.append(file_a)
                        image_files.append(file_b)

                        if self.split_reverse:
                            logger.debug("Reverse splitted double page")
                            file_a, file_b = file_b, file_a

                        half_width = int(pic.size[0] / 2)
                        pic.crop((0, 0, half_width, (pic.size[1]))).save(file_a)
                        pic.crop((half_width, 0, (pic.size[0]), (pic.size[1]))).save(file_b)

                        os.remove(file)

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

    @staticmethod
    def prepend_zeroes(current_image_idx, total_images):
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

        if not os.path.exists(os.path.dirname(image_full_path)):
            try:
                os.makedirs(os.path.dirname(image_full_path))
                logger.debug("File created : %s", image_full_path)
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

        try:
            WebDriverWait(self.driver, 10).until(
                ec.presence_of_element_located(
                    (By.CSS_SELECTOR, "div#single-reader img")
                )
            )
        except TimeoutException:
            if self.retries:
                # try again and again and again
                time.sleep(4)
                return self.download_page(chapter_path, page_url, index, total)
            else:
                raise

        image_element = self.driver.find_element_by_css_selector("div#single-reader img")

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
