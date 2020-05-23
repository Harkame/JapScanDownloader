import argparse
import shutil

import logging

logger = logging.getLogger(__name__)


def get_arguments(arguments):
    argument_parser = argparse.ArgumentParser(
        description="Script to download mangas from JapScan",
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999),
    )

    argument_parser.add_argument(
        "-c",
        "--config_file",
        help="Set config file"
        "{os.linesep}"
        "Example : python japscandownloader/main.py -c /home/myconfigfile.yml",
    )

    argument_parser.add_argument(
        "-D",
        "--driver",
        default=shutil.which("chromedriver"),
        help="""
    Chrome web driver
    Example : python japscandownloader/main.py -d C:\chromedriver.exe""",
    )

    argument_parser.add_argument(
        "-d",
        "--destination_path",
        help="Set destination path of downloaded mangas"
        "Example : python japscandownloader/main.py -d /home/mymangas/",
    )

    argument_parser.add_argument(
        "-f",
        "--format",
        help="Set format of downloaded mangas"
        "Example : python japscandownloader/main.py -f cbz|pdf|jpg|png",
    )

    argument_parser.add_argument(
        "-v",
        "--verbose",
        help="Active verbose mode, support different level"
        "Example : python japscandownloader/main.py -vv",
        action="count",
    )

    argument_parser.add_argument(
        "-r",
        "--reverse",
        help="Reverse chapters download order"
        "Default : Last to first"
        "Example : python japscandownloader/main.py -r",
        action="count",
    )

    argument_parser.add_argument(
        "-k",
        "--keep",
        help="Keep downloaded images (when format is pdf/cbz)"
        "Default : false"
        "Example : python japscandownloader/main.py -k",
        action="count",
    )

    return argument_parser.parse_args(arguments)
