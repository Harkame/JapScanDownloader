import argparse
import os

def get_arguments(arguments):
    argument_parser = argparse.ArgumentParser(description='Script to download mangas from JapScan',
    formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))

    argument_parser.add_argument(
        '-c', '--config_file',
        help = f"Set config file"
                "{os.linesep}"
                "Example : python japscandownloader/main.py -c /home/myconfigfile.yml",
        type = str
    )

    argument_parser.add_argument(
        '-d', '--destination_path',
        help = f"Set destination path of downloaded mangas"
                "Example : python japscandownloader/main.py -d /home/mymangas/",
        type = str,
    )

    argument_parser.add_argument(
        '-f', '--format',
        help = f"Set format of downloaded mangas"
                "Example : python japscandownloader/main.py -f cbz|pdf|jpg|png",
        type = str,
    )

    argument_parser.add_argument(
        '-v', '--verbose',
        help = f"Active verbose mode, support different level"
                "Example : python japscandownloader/main.py -vv",
        action = 'count',
    )

    argument_parser.add_argument(
        '-r', '--reverse',
        help = f"Reverse chapters download order"
                "Default : Last to first"
                "Example : python japscandownloader/main.py -r",
        action = 'count',
    )

    argument_parser.add_argument(
        '-k', '--keep',
        help = f"Keep downloaded images (when format is pdf/cbz)"
                "Default : false"
                "Example : python japscandownloader/main.py -k",
        action = 'count',
    )

    argument_parser.add_argument(
        '-u', '--unscramble',
        help = "Force unscrambling"
                "Example : python japscandownloader/main.py -u",
        action = 'count',
    )

    return argument_parser.parse_args(arguments)
