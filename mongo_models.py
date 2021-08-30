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
        if self.collection.find({'id': obj._id}).count():
            return self.collection.update({"id": obj._id}, obj.json)
        else:
            return self.save(obj)

    def remove(self, obj=None, mid=None):
        if obj:
            mid = obj._id
        if self.collection.find({'_id': mid}).count():
            return self.collection.delete_many({"_id": mid})
        raise NoObjectWithIdException()

    def find_all(self):
        col = []
        for s in self.collection.find():
            col.append(Scenario(json=s))
        return col

