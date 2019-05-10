from yaml import Loader, load

def get_config(config_file_path):
    config_stream = open(config_file_path, 'r')

    config_file = load(config_stream, Loader=Loader)

    config_stream.close()

    return config_file;
