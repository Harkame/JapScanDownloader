import argparse
import os

from argparse import RawTextHelpFormatter

def get_arguments(arguments):
    argument_parser = argparse.ArgumentParser(description='Script to download mangas from JapScan',
    formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))

    argument_parser.add_argument(
        '-c', '--config_file',
        help = 'Set config file' + os.linesep + 'Example : python japscandownloader/main.py -c /home/myconfigfile.yml',
        type = str
    )

    argument_parser.add_argument(
        '-d', '--destination_path',
        help = 'Set destination path of downloaded mangas' + os.linesep + 'Example : python japscandownloader/main.py -d /home/mymangas/',
        type = str,
    )

    argument_parser.add_argument(
        '-f', '--format',
        help = 'Set format of downloaded mangas' + os.linesep + 'Example : python japscandownloader/main.py -f cbz|pdf|jpg|png',
        type = str,
    )

    argument_parser.add_argument(
        '-v', '--verbose',
        help = 'Active verbose mode, support different level' + os.linesep + 'Example : python japscandownloader/main.py -vv',
        action = 'count',
    )

    argument_parser.add_argument(
        '-r', '--reverse',
        help = 'Reverse chapters download order' + os.linesep + 'Default : Last to first' + os.linesep + 'Example : python japscandownloader/main.py -r',
        action = 'count',
    )

    argument_parser.add_argument(
        '-k', '--keep',
        help = 'Keep downloaded images (when format is pdf/cbz)' + os.linesep + 'Default : false' + os.linesep + 'Example : python japscandownloader/main.py -k',
        action = 'count',
    )

    argument_parser.add_argument(
        '-u', '--unscramble',
        help = 'Force unscrambling' + os.linesep + 'Example : python japscandownloader/main.py -u',
        action = 'count',
    )

    return argument_parser.parse_args(arguments)
