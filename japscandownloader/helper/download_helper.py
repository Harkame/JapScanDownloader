from helper.format_helper import create_cbz, create_pdf, delete_images
from helper.unscramble_helper import unscramble_image
from urlparse import urlparse

import settings.settings as settings

from bs4 import BeautifulSoup
import os
from tqdm import tqdm

JAPSCAN_URL = 'https://www.japscan.to'

def download_manga(scraper, manga):
    if 'url' in manga:
        chapter_divs = BeautifulSoup(scraper.get(manga['url']).content, features='lxml').findAll('div',{'class':'chapters_list text-truncate'});

        #chapters_progress_bar = tqdm(total=len(chapter_divs), position=0, bar_format='[{bar}] - [{n_fmt}/{total_fmt}] - [chapters]')

        chapters = None

        if settings.reverse:
            chapters = reversed(chapter_divs)
        else:
            chapters = chapter_divs

        for chapter_div in chapters:
            chapter_tag = chapter_div.find(href=True)

            chapter_name = chapter_tag.contents[0].replace('\t', '').replace('\n', '')

            settings.logger.debug('chapter_name : %s', chapter_name)

            chapter_url = JAPSCAN_URL + chapter_tag['href']

            download_chapter(scraper, chapter_url)

        #chapters_progress_bar.close()

    elif 'chapters' in manga:
        base_counter = manga['chapters']['chapter_min']
        while base_counter <= manga['chapters']['chapter_max']:
            download_chapter(scraper, manga['chapters']['url'] + str(base_counter) + "/")
            base_counter += 1
    else:
        download_chapter(scraper, manga['chapter'])

def download_chapter(scraper, chapter_url):
    settings.logger.debug('chapter_url : %s', chapter_url)

    pages = BeautifulSoup(scraper.get(chapter_url).content, features='lxml').find('select', {'id': 'pages'})

    page_options = pages.findAll('option', value=True)

    pages_progress_bar = tqdm(total=len(page_options), position=1, bar_format='[{bar}] - [{n_fmt}/{total_fmt}] - [pages]')

    data = chapter_url.split('/')

    settings.logger.debug('data : %s', str(data))

    manga_name = data[4]
    chapter_number = data[5]

    chapter_path = os.path.join(settings.destination_path, manga_name, chapter_number)

    for page_tag in page_options:
        page_url = JAPSCAN_URL + page_tag['value']

        settings.logger.debug('page_url : %s', page_url)

        download_page(scraper, chapter_path, page_url)

        pages_progress_bar.update(1)

    pages_progress_bar.close()

    if settings.manga_format == 'pdf':
        create_pdf(chapter_path, os.path.join(chapter_path, chapter_number + '.pdf'))
        if not settings.keep:
            delete_images(chapter_path)

    elif settings.manga_format == 'cbz':
        create_cbz(chapter_path, os.path.join(chapter_path, chapter_number + '.cbz'))
        if not settings.keep:
            delete_images(chapter_path)

def download_page(scraper, chapter_path , page_url):
    settings.logger.debug('page_url: %s', page_url)

    page = BeautifulSoup(scraper.get(page_url).content, features='lxml')

    image_url = page.find('div', {'id': 'image'})['data-src']

    settings.logger.debug('image_url: %s', image_url)

    unscramble = False

    if 'clel' in image_url:
        settings.logger.debug('scrambled image')
        unscramble = True

    image_name = urlparse(image_url).path.split('/')[-1]

    image_full_path = os.path.join(chapter_path, image_name)

    settings.logger.debug('image_full_path : %s', image_full_path)

    if not os.path.exists(os.path.dirname(image_full_path)):
        try:
            os.makedirs(os.path.dirname(image_full_path))
            settings.logger.debug('File created : %s', image_full_path)
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
