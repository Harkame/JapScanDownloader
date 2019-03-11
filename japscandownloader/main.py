from bs4 import BeautifulSoup #html parsing
import cfscrape #bypass cloudflare
import errno #makedirs error
import os #makedirs, path, etc
from tqdm import tqdm #progress bar
import logging #logs

import sys #sys.args sys.exit

from helper.unscramble_helper import unscramble_image #unscramble method
from helper.config_helper import get_config #helper config
from helper.argument_helper import get_arguments #helper arguments
from helper.format_helper import create_cbz, create_pdf

JAPSCAN_URL = 'https://www.japscan.to'
DEFAULT_CONFIG_FILE = os.path.join('.', 'config.yml')
DEFAULT_DESTINATION_PATH = os.path.join('.', 'mangas')
DEFAULT_MANGA_FORMAT = 'jpg'

manga_format = None

def main():
    logger = logging.getLogger()
    config_file = DEFAULT_CONFIG_FILE
    destination_path = None
    manga_format = None

    arguments = get_arguments(sys.argv[1:])

    if arguments.verbose:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(module)s :: %(lineno)s :: %(funcName)s :: %(message)s')
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

    config = get_config(config_file)

    mangas = []

    if config['mangas'] is not None:
        mangas = config['mangas']

    if destination_path is None:
        if config['destinationPath'] is not None:
            destination_path = config['destinationPath']
        else:
            destination_path = DEFAULT_DESTINATION_PATH

    if manga_format is None:
        if config['mangaFormat'] is not None:
            manga_format = config['mangaFormat']
        else:
            manga_format = DEFAULT_MANGA_FORMAT

    logger.debug('mangas : %s', mangas)
    logger.debug('destination_path : %s', destination_path)
    logger.debug('manga_format : %s', manga_format)

    scraper = cfscrape.create_scraper()

    for manga in mangas:
        chapter_divs = BeautifulSoup(scraper.get(manga['url']).content, features='lxml').findAll('div',{'class':'chapters_list text-truncate'});

        chapters_progress_bar = tqdm(total=len(chapter_divs), position=0, bar_format='[{bar}] - [{n_fmt}/{total_fmt}] - [chapters]')

        for chapter_div in chapter_divs:
            chapter_tag = chapter_div.find(href=True)

            chapter_ref = JAPSCAN_URL + chapter_tag['href']

            chapter_name = chapter_tag.contents[0].replace('\t', '').replace('\n', '')

            logger.debug('chapter_ref : %s', chapter_ref)

            logger.debug('chapter_name : %s', chapter_name)

            pages = BeautifulSoup(scraper.get(chapter_ref).content, features='lxml').find('select', {'id': 'pages'})

            page_options = pages.findAll('option', value=True)

            pages_progress_bar = tqdm(total=len(page_options), position=1, bar_format='[{bar}] - [{n_fmt}/{total_fmt}] - [pages]')

            chapter_path = ''

            for page_tag in page_options:
                page_url = JAPSCAN_URL + page_tag['value']

                logger.debug('page_url: %s', page_url)

                page = BeautifulSoup(scraper.get(page_url).content, features='lxml')

                image_url = page.find('div', {'id': 'image'})['data-src']

                logger.debug('image_url: %s', image_url)

                unscramble = False

                if 'clel' in image_url:
                    logger.debug('scrambled image')
                    unscramble = True

                reverse_image_url = image_url[::-1]

                slash_counter = 0
                index = 0

                while slash_counter < 3:
                    if reverse_image_url[index] == '/':
                        slash_counter += 1
                    index += 1

                reverse_image_url = reverse_image_url[0:index]

                image_path = reverse_image_url[::-1]

                logger.debug('image_path : %s', image_path)

                image_full_path = destination_path + image_path

                logger.debug('image_full_path : %s', image_full_path)

                data = image_path.split('/')

                logger.debug('data : %s', str(data))

                manga_name = data[1]
                chapter_number = data[2]

                chapter_path = os.path.join(destination_path, manga_name, chapter_number)

                if not os.path.exists(os.path.dirname(image_full_path)):
                    try:
                        os.makedirs(os.path.dirname(image_full_path))
                        logger.debug('File created : %s', image_full_path)
                    except OSError as exc:
                        if exc.errno != errno.EEXIST:
                            raise

                image_content = scraper.get(image_url).content

                if unscramble is True:
                    scrambled_image = image_full_path + '_scrambled'
                else:
                    scrambled_image = image_full_path

                file = open(scrambled_image, 'wb')

                file.write(image_content)

                file.close()

                if unscramble is True:
                    unscramble_image(scrambled_image, image_full_path)
                    os.remove(scrambled_image)

                pages_progress_bar.update(1)

            if manga_format == 'pdf':
                create_pdf(chapter_path, os.path.join(chapter_path, chapter_number + '.pdf'))
            elif manga_format == 'cbz':
                create_cbz(chapter_path, os.path.join(chapter_path, chapter_number + '.cbz'))

            pages_progress_bar.close()

            chapters_progress_bar.update(1)

        chapters_progress_bar.close()

if __name__ == '__main__':
    main()
