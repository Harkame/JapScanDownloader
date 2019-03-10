import argparse

def get_arguments(arguments):
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

    return argument_parser.parse_args(arguments)
