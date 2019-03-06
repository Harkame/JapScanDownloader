import config.config as config

import argparse #argument parser
import logging #logs

def get_arguments():
    argument_parser = argparse.ArgumentParser()

    argument_parser.add_argument(
        '-c', '--config.config_file',
        help='Set config file',
        type=str,
    )

    argument_parser.add_argument(
        '-d', '--config.destination_path',
        help='Set destination path of downloaded config.mangas',
        type=str,
    )

    argument_parser.add_argument(
        '-f', '--format',
        help='Set format of downloaded config.mangas',
        default=logging.WARNING,
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
        config.logger = logging.getLogger()
        config.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
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
