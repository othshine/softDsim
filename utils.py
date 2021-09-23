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


def dots(n: int):
    """
    Returns a string with n dots: •
    :param n: int - number of desired dots
    :return: str - •••
    """
    return "•" * n


def month_to_day(value: float, num_days: int = 1) -> float:
    """
    Turns a value that refers to a timespan of one month to the time in days. Assumes that a month is 20 business
    days long. :param value: e.g. 3000 ($ per month) :param num_days: e.g. 15 (days) :return: 1500 ($ per 15 days)
    """
    return value * (num_days / 20)


def data_get(data, title) -> dict:
    """
    Searches in list data for a dict that has a attr 'title' that equals <title>.
    :param data: A list of dicts.
    :param title: A string that is the title of the dict that is searched.
    :return: dict
    """
    for obj in data:
        if obj.get('title') == title:
            return obj
    return {}


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
