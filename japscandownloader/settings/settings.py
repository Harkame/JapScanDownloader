import logging
import os
import sys

from helper.argument_helper import get_arguments
from helper.config_helper import get_config

DEFAULT_CONFIG_FILE = os.path.join('.', 'config.yml')
DEFAULT_DESTINATION_PATH = os.path.join('.', 'mangas')
DEFAULT_MANGA_FORMAT = 'jpg'

logger = logging.getLogger()
config_file = None
destination_path = None
keep = False
manga_format = None
reverse = False
unscramble = False
mangas = []

def init(arguments):
    global logger

    global config_file
    global destination_path
    global keep
    global manga_format
    global unscramble
    global reverse

    global mangas

    config_file = DEFAULT_CONFIG_FILE

    init_arguments(arguments)

    mangas = init_config()

    logger.debug('config_file : %s', config_file)
    logger.debug('destination_path : %s', destination_path)
    logger.debug('keep : %s', keep)
    logger.debug('manga_format : %s', manga_format)
    logger.debug('unscramble : %s', unscramble)
    logger.debug('reverse : %s', reverse)

    logger.debug('mangas : %s', mangas)
    
def init_arguments(arguments):
    global logger

    global config_file
    global destination_path
    global keep
    global manga_format
    global reverse
    global unscramble

    global mangas

    arguments = get_arguments(arguments)

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

    if arguments.reverse:
        reverse = True

    if arguments.keep:
        keep = True

    if arguments.keep:
        unscramble = True

def init_config():
    global logger

    global config_file
    global destination_path
    global keep
    global manga_format
    global reverse
    global unscramble

    global mangas

    config = get_config(config_file)

    if config['mangas'] is not None:
        mangas = config['mangas']

    if destination_path is None:
        if config['destination_path'] is not None:
            destination_path = config['destination_path']
        else:
            destination_path = DEFAULT_DESTINATION_PATH

    if manga_format is None:
        if config['manga_format'] is not None:
            manga_format = config['manga_format']
        else:
            manga_format = DEFAULT_MANGA_FORMAT
