import os #path

JAPSCAN_URL = 'https://www.japscan.to'
DEFAULT_CONFIG_FILE = os.path.join('.', 'config.yml')
DEFAULT_DESTINATION_PATH = os.path.join('.', 'mangas')
DEFAULT_MANGA_FORMAT = 'jpg'

config_file = None
destination_path = None
manga_format = None

mangas = []

logger = None
