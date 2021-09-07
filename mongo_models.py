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

    def get(self, _id):
        if json := self.collection.find_one({'_id': _id}):
            return Scenario(json=json)
        raise NoObjectWithIdException()

    def save(self, obj) -> ObjectId:
        return self.collection.insert_one(obj.json).inserted_id

    def update(self, obj):  # ToDo: Tests for updating Scenarios.
        if self.collection.find({'_id': obj.get_id()}).count():
            self.remove(mid=obj.get_id())
        return self.save(obj)

    def remove(self, obj=None, mid=None):
        if obj:
            mid = obj.get_id
        if self.collection.find({'_id': mid}).count():
            return self.collection.delete_many({"_id": mid})
        raise NoObjectWithIdException()

    def find_all(self):
        col = []
        for s in self.collection.find():
            col.append(Scenario(json=s))
        return col

