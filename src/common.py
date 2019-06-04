import os.path
from configparser import ConfigParser
from collections import OrderedDict


def ini_to_dict(path):
    """

    Read an ini path in to a dict
    :param path: Path to file
    :return: an OrderedDict of that path ini data
    """
    config = ConfigParser()
    config.read(path)
    return_value = OrderedDict()
    for section in reversed(config.sections()):
        return_value[section] = OrderedDict()
        section_tuples = config.items(section)
        for item_turple in reversed(section_tuples):
            return_value[section][item_turple[0]] = item_turple[1]
    return return_value


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "conf" ,"config.ini")


def get_config():
    return ini_to_dict(CONFIG_PATH)

def get_uri(settings):
    return "sqlite:///" + settings["db"]["db_name"] + ".db"
