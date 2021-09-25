from bson import ObjectId
from deprecated.classic import deprecated
from pymongo import MongoClient

from app.src.domain.factories import Factory
from app.src.domain.scenario import Scenario, UserScenario


class NoObjectWithIdException(Exception):
    pass


class MongoConnection(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client['v2']

    def get_collection(self, name):
        self.collection = self.db[name]


class ScenarioMongoModel(MongoConnection):
    def __init__(self):
        super(ScenarioMongoModel, self).__init__()
        self.get_collection('scenarios')

    def get(self, _id):
        typ = 'scenario'
        if json := self.collection.find_one({'_id': _id}):
            if json.get('template') is None:
                typ = 'userscenario'
                json['template'] = self.get(json.get('template_id'))
            return Factory.deserialize(json, typ)
        raise NoObjectWithIdException()

    def save(self, obj) -> ObjectId:
        if isinstance(obj, Scenario):
            obj = obj.json
        return self.collection.insert_one(obj).inserted_id

    def save_template(self, obj) -> ObjectId:
        return self.collection.insert_one({**obj.json, 'template': True}).inserted_id

    def update(self, obj):  # ToDo: Tests for updating Scenarios.
        # ToDo: Do not allow to update templates.
        print(obj.json)
        return self.collection.find_one_and_update({'_id': obj.get_id()}, {"$set": obj.json})['_id']

    def remove(self, obj=None, mid=None):
        if obj:
            mid = obj.get_id
        if self.collection.find({'_id': mid}).count():
            return self.collection.delete_many({"_id": mid})
        raise NoObjectWithIdException()

    def find_all_templates(self):
        col = []
        for s in self.collection.find({'template': True}):
            col.append(Factory.deserialize(json=s, typ="scenario"))
        return col

    @deprecated
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

    def create(self, sid, user):
        if template := self.collection.find_one({'_id': sid}):
            return self.save(Factory.create_user_scenario(user, template).json)
        raise NoObjectWithIdException("No template scenario with id: " + str(sid))
