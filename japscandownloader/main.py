from bs4 import BeautifulSoup #html parsing
import cfscrape #bypass cloudflare
import errno #makedirs error
import os #makedirs, path, etc
from tqdm import tqdm #progress bar

from unscramble.unscramble import unscramble_image #unscramble method

from manga_format.manga_format_cbz import create_cbz #manga format cbz archive
from manga_format.manga_format_pdf import create_pdf #manga format pdf

import config.config as config #all global variables and constants

from helper.config_helper import get_config
from helper.argument_helper import get_arguments

def main():
    get_arguments()

    get_config()

    config.logger.debug(config.mangas)
    config.logger.debug(config.destination_path)
    config.logger.debug(config.manga_format)

    scraper = cfscrape.create_scraper()

    for manga in config.mangas:
        chapter_divs = BeautifulSoup(scraper.get(manga['url']).content, features='lxml').findAll('div',{'class':'chapters_list text-truncate'});

        chapters_progress_bar = tqdm(total=len(chapter_divs), position=0, bar_format='[{bar}] - [{n_fmt}/{total_fmt}] - [chapters]')

        for chapter_div in chapter_divs:
            chapter_tag = chapter_div.find(href=True)

            chapter_ref = JAPSCAN_URL + chapter_tag['href']

            chapter_name = chapter_tag.contents[0].replace('\t', '').replace('\n', '')

            config.logger.debug('chapter_ref : %s', chapter_ref)

            config.logger.debug('chapter_name : %s', chapter_name)

            pages = BeautifulSoup(scraper.get(chapter_ref).content, features='lxml').find('select', {'id': 'pages'})

            page_options = pages.findAll('option', value=True)

            pages_progress_bar = tqdm(total=len(page_options), position=1, bar_format='[{bar}] - [{n_fmt}/{total_fmt}] - [pages]')

            chapter_path = ''

            for page_tag in page_options:
                page_url = JAPSCAN_URL + page_tag['value']

                config.logger.debug('page_url: %s', page_url)

                page = BeautifulSoup(scraper.get(page_url).content, features='lxml')

                image_url = page.find('div', {'id': 'image'})['data-src']

                config.logger.debug('image_url: %s', image_url)

                unscramble = False

                if 'clel' in image_url:
                    config.logger.debug('scrambled image')
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

                config.logger.debug('image_path : %s', image_path)

                image_full_path = config.destination_path + image_path

                config.logger.debug('image_full_path : %s', image_full_path)

                data = image_path.split('/')

                config.logger.debug('data : %s', str(data))

                manga_name = data[1]
                chapter_number = data[2]
                file_name = data[3];

                chapter_path = os.path.join(config.destination_path, manga_name, chapter_number)

                if not os.path.exists(os.path.dirname(image_full_path)):
                    try:
                        os.makedirs(os.path.dirname(image_full_path))
                        config.logger.debug('File created : %s', image_full_path)
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

            if config.manga_format == 'pdf':
                create_pdf(chapter_path, os.path.join(chapter_path, chapter_number + '.pdf'))
            elif config.manga_format == 'cbz':
                create_cbz(chapter_path, os.path.join(chapter_path, chapter_number + '.cbz'))

            pages_progress_bar.close()

            chapters_progress_bar.update(1)

        chapters_progress_bar.close()

if __name__ == '__main__':
    main()
