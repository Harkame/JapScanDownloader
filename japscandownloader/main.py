from bs4 import BeautifulSoup #html parsing
import cfscrape #bypass cloudflare
import errno #makedirs error
import logging #logs
import getopt, sys #get options
import os #makedirs
from tqdm import tqdm #progress bar
from yaml import Loader, load #config file

from usage.usage import usage #usage method
from unscramble.unscramble import unscramble_image #unscramble method

from manga_format.manga_format_cbz import create_cbz #manga format cbz archive
from manga_format.manga_format_pdf import create_pdf #manga format pdf

JAPSCAN_URL = 'https://www.japscan.to'
DEFAULT_CONFIG_FILE = os.path.join('.', 'config.yml')
DEFAULT_DESTINATION_PATH = os.path.join('.', 'mangas')
DEFAULT_MANGA_FORMAT = 'jpg'

config_file = None
destination_path = None
manga_format = None

mangas = []

def get_options():
    try:
        options, arguments = getopt.getopt(sys.argv[1:], 'cdf:hv', ['config', 'destination_path', 'format', 'help', 'verbose'])
        logging.debug('arguments : %s', arguments)
    except getopt.GetoptError as error:
        logging.error(error)
        usage()

    global config_file
    global destination_path
    global manga_format

    for option, argument in options:
        if option in ('-c', '--config'):
            config_file = argument
            logging.debug('option config_file : %s', config_file)
        elif option in ('-d', '--destination_path'):
            destination_path = argument
            logging.debug('option destinationPath : %s', destination_path)
        elif option in ('-f', '--format'):
            manga_format = argument
            logging.debug('option mangaFormat : %s', manga_format)
        elif option in ('-h', '--help'):
            usage()
            sys.exit()
        elif option in('-v', '--verbose'):
            logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
            logging.debug('option verbose')

def get_config():
    global config_file
    global destination_path
    global manga_format
    global mangas

    if config_file is None:
        config_file = DEFAULT_CONFIG_FILE

    config_stream = open(config_file, 'r')

    config = load(config_stream, Loader=Loader)

    config_stream.close()

    if config['mangas'] is not None:
        mangas.extend(config['mangas'])
        logging.debug('mangas : %s', mangas)

    if destination_path is None:
        if config['destinationPath'] is not None:
            destination_path = config['destinationPath']
            logging.debug('destination_path : %s', destination_path)
        else:
            destination_path = DEFAULT_DESTINATION_PATH

    if manga_format is None:
        if config['mangaFormat'] is not None:
            manga_format = config['mangaFormat']
            logging.debug('manga_format : %s', manga_format)
        else:
            manga_format = DEFAULT_MANGA_FORMAT

def main():
    get_options()

    get_config()

    global mangas
    global destination_path
    global manga_format

    scraper = cfscrape.create_scraper()

    for manga in mangas:
        chapter_divs = BeautifulSoup(scraper.get(manga['url']).content, features='lxml').findAll('div',{'class':'chapters_list text-truncate'});

        chapters_progress_bar = tqdm(total=len(chapter_divs), position=0, bar_format='[{bar}] - [{n_fmt}/{total_fmt}] - [chapters]')

        for chapter_div in chapter_divs:
            chapter_tag = chapter_div.find(href=True)

            chapter_ref = JAPSCAN_URL + chapter_tag['href']

            chapter_name = chapter_tag.contents[0].replace('\t', '').replace('\n', '')

            logging.debug('chapter_ref : %s', chapter_ref)

            logging.debug('chapter_name : %s', chapter_name)

            pages = BeautifulSoup(scraper.get(chapter_ref).content, features='lxml').find('select', {'id': 'pages'})

            page_options = pages.findAll('option', value=True)

            pages_progress_bar = tqdm(total=len(page_options), position=1, bar_format='[{bar}] - [{n_fmt}/{total_fmt}] - [pages]')

            chapter_path = ''

            for page_tag in page_options:
                page_url = JAPSCAN_URL + page_tag['value']

                logging.debug('page_url: %s', page_url)

                page = BeautifulSoup(scraper.get(page_url).content, features='lxml')

                image_url = page.find('div', {'id': 'image'})['data-src']

                logging.debug('image_url: %s', image_url)

                unscramble = False

                if 'clel' in image_url:
                    logging.debug('scrambled image')
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

                logging.debug('image_path : %s', image_path)

                image_full_path = destination_path + image_path

                logging.debug('image_full_path : %s', image_full_path)

                data = image_path.split('/')

                logging.debug('data : %s', str(data))

                manga_name = data[1]
                chapter_number = data[2]
                file_name = data[3];

                chapter_path = os.path.join(destination_path, manga_name, chapter_number)

                if not os.path.exists(os.path.dirname(image_full_path)):
                    try:
                        os.makedirs(os.path.dirname(image_full_path))
                        logging.debug('File created : %s', image_full_path)
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

if __name__ == "__main__":
    main()
