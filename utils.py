from pymongo import MongoClient
from yaml import load, FullLoader


def get_db_handle(db_name, host, port):
    client = MongoClient(host=host,
                         port=int(port)
                         )
    db_handle = client[db_name]
    return db_handle, client


class YAMLReader:
    def __init__(self, path):
        self.path = path

    def read(self, *args):
        with open(self.path) as y:
            data = load(y, Loader=FullLoader)
            for arg in args:
                data = data[arg]
        return data
