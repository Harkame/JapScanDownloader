import logging #logs

def init():
    global logger
    global destination_path
    global remove
    global manga_format

    logger = logging.getLogger()
    destination_path = None
    remove = False
    manga_format = None
