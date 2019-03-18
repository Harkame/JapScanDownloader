import logging #logs

logger = logging.getLogger()
config_file = None
destination_path = None
remove = True
manga_format = None

def init():
    global logger
    global config_file
    global destination_path
    global remove
    global manga_format
