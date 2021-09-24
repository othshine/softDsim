from bson import ObjectId
from pymongo import MongoClient

from app.src.domain.decision_tree import Scenario


class NoObjectWithIdException(Exception):
    pass


class MongoConnection(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
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
        if isinstance(obj, Scenario):
            obj = obj.json
        return self.collection.insert_one(obj).inserted_id

    def save_template(self, obj) -> ObjectId:
        return self.collection.insert_one({**obj.json, 'template': True}).inserted_id

    def update(self, obj):  # ToDo: Tests for updating Scenarios.
        self.collection.find_one_and_update({'_id': obj.get_id()}, { "$set" : obj.json})
        """
        if self.collection.find().count():
            self.remove(mid=obj.get_id())
        return self.save(obj)
        """

    def remove(self, obj=None, mid=None):
        if obj:
            mid = obj.get_id
        if self.collection.find({'_id': mid}).count():
            return self.collection.delete_many({"_id": mid})
        raise NoObjectWithIdException()

    def find_all_templates(self):
        col = []
        for s in self.collection.find({'template': True}):
            col.append(Scenario(json=s))
        return col

    def copy(self, sid, user: str):
        if json := self.collection.find_one({'_id': sid}):
            i = str(ObjectId())
            json['id'] = i
            json['_id'] = i
            json['user'] = user
            json['template'] = False
            return self.save(json)
        raise NoObjectWithIdException()

    def find_user_scores(self, name, username):
        f = {"name": name, "user": username}
        result = list(self.collection.find(f))
        tries = len(result)
        best_score = 0
        for s in result:
            best_score = max(best_score, Scenario(json=s).total_score())
        return tries, best_score

