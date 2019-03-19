import argparse
import os

def get_arguments(arguments):
    argument_parser = argparse.ArgumentParser()

    argument_parser.add_argument(
        '-c', '--config_file',
        help = 'Set config file' + os.linesep + 'Example : python japscandownloader/main.py -c /home/myconfigfile.yml',
        type = str,
    )

    argument_parser.add_argument(
        '-d', '--destination_path',
        help = 'Set destination path of downloaded mangas' + os.linesep + 'Example : python japscandownloader/main.py -d /home/mymangas/',
        type = str,
    )

    argument_parser.add_argument(
        '-f', '--format',
        help = 'Set format of downloaded mangas' + os.linesep + 'Example : python japscandownloader/main.py -f cbz',
        type = str,
    )

    argument_parser.add_argument(
        '-v', '--verbose',
        help = 'Active verbose mode, support different level' + os.linesep + 'Example : python japscandownloader/main.py -vv',
        action = 'count',
    )

    argument_parser.add_argument(
        '-R', '--remove',
        help = 'remove downloaded images (when format is pdf/cbz) (default : true)' + os.linesep + 'Example : python japscandownloader/main.py -e false|f|no|n|0',
        default = True,
        type = str,
    )

    return argument_parser.parse_args(arguments)
