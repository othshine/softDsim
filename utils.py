from pymongo import MongoClient
from yaml import load, FullLoader
import os
from django.conf import settings


def get_db_handle(db_name, host, port):
    client = MongoClient(host=host,
                         port=int(port)
                         )
    db_handle = client[db_name]
    return db_handle, client


def value_or_error(val, lower: float = 0.0, upper: float = 1.0):
    """
    Used to validate that numeric value is in bound.
    :param val: the value that need to be validated.
    :param lower: lower bound
    :param upper: upper bound
    :return: either value if in bounds or raises ValueError
    """
    if lower <= val <= upper:
        return val
    raise ValueError


class _YAMLReader:
    def __init__(self, path):
        self.path = path

    def read(self, *args):
        with open(self.path) as y:
            data = load(y, Loader=FullLoader)
            for arg in args:
                data = data[arg]
        return data


YAMLReader = _YAMLReader(path=os.path.join(settings.BASE_DIR, 'parameter.yaml'))
