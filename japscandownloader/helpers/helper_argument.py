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
        help="Set config file\n"
             "Example : python japscandownloader/main.py -c /home/myconfigfile.yml",
    )

    argument_parser.add_argument(
        "-D",
        "--driver",
        default=shutil.which("chromedriver"),
        help="""Chrome web driver
Example : python japscandownloader/main.py -D C:\\chromedriver.exe""",
    )

    argument_parser.add_argument(
        "-d",
        "--destination_path",
        help="Set destination path of downloaded mangas\n"
             "Example : python japscandownloader/main.py -d /home/mymangas/",
    )

    argument_parser.add_argument(
        "-f",
        "--format",
        help="Set format of downloaded mangas\n"
             "Example : python japscandownloader/main.py -f cbz|pdf|jpg|png",
    )

    argument_parser.add_argument(
        "-v",
        "--verbose",
        help="Active verbose mode, support different level\n"
             "Example : python japscandownloader/main.py -vv",
        action="count",
    )

    argument_parser.add_argument(
        "-r",
        "--reverse",
        help="Reverse chapters download order\n"
             "Default : Last to first\n"
             "Example : python japscandownloader/main.py -r",
        action="count",
    )

    argument_parser.add_argument(
        "-k",
        "--keep",
        help="Keep downloaded images (when format is pdf/cbz)\n"
             "Default : false\n"
             "Example : python japscandownloader/main.py -k",
        action="count",
    )

    argument_parser.add_argument(
        "-p",
        "--profile",
        help="Chrome profile path\n"
             "Example with Windows : python -p C:\\Users\\Me\\AppData\\Local\\Google\\Chrome\\User Data\n"
             "Be careful, you can't use your normal chrome browser and this parameter at same time\n"
             "(user data directory is already in use)",
    )

    argument_parser.add_argument("-s", "--show", help="Show browser", action="count")

    argument_parser.add_argument(
        "-S",
        "--split",
        help="Split double pages, reverse order with -SS\n"
             "Default : false\n"
             "Example split : python japscandownloader/main.py -S\n"
             "Example split and reverse: python japscandownloader/main.py -SS",
        action="count"
    )

    argument_parser.add_argument(
        "-R",
        "--retries",
        help="Infinite retries in case of timeout\n"
             "Default : false\n"
             "Example : python japscandownloader/main.py -R",
        action="count",
    )

    return argument_parser.parse_args(arguments)
