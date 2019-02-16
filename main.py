from bs4 import BeautifulSoup #html parsing
import cfscrape #bypass cloudflare
import errno #makedirs error
import logging #logs
import getopt, sys #get options
import os #makedirs
from tqdm import tqdm #progress bar
from yaml import Loader, load #config file

JAPSCAN_URL = 'https://www.japscan.to'
DEFAULT_CONFIG_FILE = './config.yaml'
DEFAULT_DESTINATION_PATH = './mangas'

config_file = DEFAULT_CONFIG_FILE
destination_path = DEFAULT_DESTINATION_PATH

def usage():
    print('Usage')

try:
    opts, args = getopt.getopt(sys.argv[1:], 'cd:hv', ['config', 'destination_path', 'help', 'verbose'])
except getopt.GetoptError as err:
    usage()
    sys.exit(2)

output = None
verbose = False

for option, argument in opts:
    if option in ('-c', '--config'):
        config_file = argument
        logging.debug('option config_file : %s', config_file)
    elif option in ('-d', '--destination_path'):
        destination_path = argument
        logging.debug('option destinationPath : %s', destination_path)
    elif option in ('-h', '--help'):
        usage()
    elif option in('-v', '--verbose'):
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
        logging.debug('option verbose')

config_stream= open(config_file, 'r')

config = load(config_stream, Loader=Loader)

config_stream.close()

mangas = config['mangas']

if destination_path == None:
    destination_path = config['destinationPath']

logging.debug('config_file : %s', config_file)

logging.debug('destination_path : %s', destination_path)

scraper = cfscrape.create_scraper()

for manga in mangas:
    chapter_divs = BeautifulSoup(scraper.get(manga['url']).content, features='lxml').findAll('div',{'class':'chapters_list text-truncate'});

    chapters_progress_bar = tqdm(total=len(chapter_divs), position=0)

    for chapter_div in chapter_divs:
        chapter_ref = JAPSCAN_URL + chapter_div.find(href=True)['href']

        logging.debug('chapter_ref: %s', chapter_ref)

        pages = BeautifulSoup(scraper.get(chapter_ref).content, features='lxml').find('select', {'id': 'pages'})

        page_options = pages.findAll('option', value=True)

        pages_progress_bar = tqdm(total=len(page_options), position=1)

        for page_tag in page_options:
            page_url = JAPSCAN_URL + page_tag['value']

            logging.debug('page_url: %s', page_url)

            page = BeautifulSoup(scraper.get(page_url).content, features='lxml')

            image_url = page.find('div', {'id': 'image'})['data-src']

            logging.debug('image_url: %s', image_url)

            reverse_image_url = image_url[::-1]

            slash_counter = 0
            index = 0

            while slash_counter < 3:
                if reverse_image_url[index] == '/':
                    slash_counter += 1
                index += 1

            reverse_image_url = reverse_image_url[0:index]

            image_path = reverse_image_url[::-1]

            image_full_path = destination_path + image_path

            logging.debug('image_full_path : %s', image_full_path)

            if not os.path.exists(os.path.dirname(image_full_path)):
                try:
                    os.makedirs(os.path.dirname(image_full_path))
                    logging.debug('File created : %s', image_full_path)
                except OSError as exc:
                    if exc.errno != errno.EEXIST:
                        raise

            image_content = scraper.get(image_url).content

            file = open(image_full_path, 'wb')

            file.write(image_content)

            file.close()

            pages_progress_bar.update(1);

        pages_progress_bar.close()

        chapters_progress_bar.update(1)

    chapters_progress_bar.close()
