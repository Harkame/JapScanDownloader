import logging

logger = logging.getLogger()
config_file = None
destination_path = None
keep = False
manga_format = None
reverse = False

def init():
    global logger
    global config_file
    global destination_path
    global keep
    global manga_format
    global reverse
