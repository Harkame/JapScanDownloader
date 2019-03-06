import config.config as config

import argparse #argument parser
import logging #logs

def get_arguments():
    argument_parser = argparse.ArgumentParser()

    argument_parser.add_argument(
        '-c', '--config_file',
        help='Set config file',
        type=str,
    )

    argument_parser.add_argument(
        '-d', '--destination_path',
        help='Set destination path of downloaded config.mangas',
        type=str,
    )

    argument_parser.add_argument(
        '-f', '--format',
        help='Set format of downloaded config.mangas',
        type=str,
    )

    argument_parser.add_argument(
        '-v', '--verbose',
        help='Active verbose mode, support different level',
        action='count',
    )

    arguments = argument_parser.parse_args()

    if arguments.verbose:
        print(arguments.verbose)
        config.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(module)s :: %(lineno)s :: %(funcName)s :: %(message)s')
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        if arguments.verbose == 0:
            config.logger.setLevel(logging.NOTSET)
        elif arguments.verbose == 1:
            config.logger.setLevel(logging.DEBUG)
        elif arguments.verbose == 2:
            config.logger.setLevel(logging.INFO)
        elif arguments.verbose == 3:
            config.logger.setLevel(logging.WARNING)
        elif arguments.verbose == 4:
            config.logger.setLevel(logging.ERROR)
        elif arguments.verbose == 5:
            config.logger.setLevel(logging.CRITICAL)

        config.logger.addHandler(stream_handler)

    if arguments.config_file:
        config.config_file = arguments.config_file

    if arguments.destination_path:
        config.destination_path = arguments.destination_path

    if arguments.format:
        config.manga_format = arguments.format
