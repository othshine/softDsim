from bson import ObjectId
from pymongo import MongoClient

from app.src.domain.decision_tree import Scenario


class NoObjectWithIdException(Exception):
    pass


class MongoConnection(object):
    def __init__(self):
        client = MongoClient('localhost', 2717)
        self.db = client['softdsim']

    def get_collection(self, name):
        self.collection = self.db[name]


class ScenarioMongoModel(MongoConnection):
    def __init__(self):
        super(ScenarioMongoModel, self).__init__()
        self.get_collection('scenarios')

    def get(self, id_):
        if json := self.collection.find_one({'_id': id_}):
            return Scenario(json=json)
        raise NoObjectWithIdException()

    def save(self, obj) -> ObjectId:
        return self.collection.insert_one(obj.json).inserted_id

    def update(self, obj):
        if self.collection.find({'id': obj.id_}).count():
            return self.collection.update({"id": obj.id_}, obj.json)
        else:
            return self.save(obj)

    def remove(self, obj=None, mid=None):
        if obj:
            mid = obj.id_
        if self.collection.find({'id': mid}).count():
            return self.collection.delete_many({"id": mid})

