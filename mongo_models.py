from typing import List

from bson import ObjectId
from deprecated.classic import deprecated
from pymongo import MongoClient
from time import time

from app.src.domain.factories import Factory
from app.src.domain.scenario import Scenario, UserScenario


class NoObjectWithIdException(Exception):
    pass


class MongoConnection(object):
    def __init__(self):
        client = MongoClient('localhost', 2717)  # ToDo: Use env var.
        self.db = client['v5']

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

    def get_name(self, sid):
        return self.collection.find_one({'_id': sid})['name']

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

    def create(self, sid, user, history_id):
        if template := self.collection.find_one({'_id': sid}):
            return self.save(Factory.create_user_scenario(user, template, history_id).json)
        raise NoObjectWithIdException("No template scenario with id: " + str(sid))


class UserMongoModel(MongoConnection):
    def __init__(self):
        super(UserMongoModel, self).__init__()
        self.get_collection('users')

    def initiate_scenario(self, user: str, scenario_template_id: str, history_id: str, scenario_id: str):
        """Adds a 0 to a user's scenario with the given id. The purpose is that the score is only saved when the user
        finishes a scenario, to get an accurate count of tries, this method is called as soon as the user starts a
        scenario and the 0 is overwritten when the user actually finishes. """
        self._save_score(user=user, scenario_template_id=scenario_template_id, score=0, history_id=history_id, scenario_id=scenario_id)

    def save_score(self, user: str, scenario_template_id: str, score: int, scenario_id: str):
        """Saves the final score of a user for scenario with the given template id. It also removes one 0 value from
        the scoreboard for that scenario. """
        json = self._get_scores(user=user, scenario_template_id=scenario_template_id)
        if json:
            for entry in json:
                if ObjectId(entry['scenario_id']) ==  ObjectId(scenario_id):
                    entry['score'] = score
                    self.collection.find_one_and_update({'username': user}, {"$set":  {scenario_template_id: json}})

    def _save_score(self, user: str, scenario_template_id: str, score: int, history_id: str, scenario_id: str):
        """Saves a score for a given user and a given template id to the database."""
        scores = self._get_scores(scenario_template_id, user)
        scores.append({'score': score, 'history_id': history_id, 'scenario_id': scenario_id, 'time': int(time())})
        self.collection.find_one_and_update({'username': user}, {"$set": {scenario_template_id: scores}})

    def _get_scores(self, scenario_template_id, user):
        """Returns a list of scores of a user for a given scenario template id that are stored in the database."""
        if self.collection.count({'username': user}) == 0:
            self.save_user(user)
        json = self.collection.find_one({'username': user})
        scores = json.get(scenario_template_id, [])
        return scores

    def _remove_score(self, user: str, scenario_template_id: str, scenario_id: str):
        """Removes the scenario in a given user's scenario template id array from the database."""
        scores = self._get_scores(scenario_template_id, user)
        output = None
        for i, score in enumerate(scores):
            if score['scenario_id'] == scenario_id:
                print("DELETED")
                output = score
                del scores[i]
                break
        self.collection.find_one_and_update({'username': user}, {"$set": {scenario_template_id: scores}})
        return output

    def save_user(self, user: str):
        """Creates a document in the database that represents a user."""
        if self.collection.find({'username': user}).count():
            raise ValueError("User " + user + " already exists!")
        self.collection.save({'username': user})
        return

    def get_best_score(self, user: str, template_id) -> int:
        """Returns the highest value in the given scenario template id array for a given user."""
        json = self.collection.find_one({'username': user}) or {}
        return max([d.get('score', 0) for d in json.get(template_id, [{'score': 0}])])

    def get_num_tries(self, user, template_id) -> int:
        """Returns the number of entries in the given scenario template id array for a given user."""
        user = self.collection.find_one({'username': user}) or {}
        return len(user.get(template_id, []))

    def get_user_ranking(self, template_id):
        """Returns a list with each user and their high score, and total rank, for a given scenario template."""
        users = self.collection.find({}) or {}
        users = [{'username': user.get('username'), 'score': self.get_best_score(user.get('username'), template_id)} for user in users if
                 user.get(template_id, False)]
        users = sorted(users, key=lambda d: d['score'], reverse=True)
        for i in range(len(users)):
            users[i]['rank'] = i + 1
        users = {e.get('username'): {'score': e.get('score'), 'rank': e.get('rank')} for e in users}
        return users

    def get_num_total_tries(self, template_id):
        """Returns the number of entries for a given template of all user accumulated."""
        users = self.collection.find({}) or {}
        return sum([len(user.get(template_id, [])) for user in users])

    def get_user_scorecard(self, user: str, template_id: str = None):
        """Returns a list of all scores for a given user and a given template id. If no template id is given,
        it returns a dict with scores for all scenarios. """
        if template_id:
            return self._get_scores(template_id, user)
        else:
            return self.collection.find_one({'username': user}) or {}



class ClickHistoryModel(MongoConnection):
    def __init__(self):
        super(ClickHistoryModel, self).__init__()
        self.get_collection('history')

    def new_hist(self):
        return self.collection.insert_one({}).inserted_id

    def get(self, id):
        return self.collection.find_one({'_id': id})

    def add_event(self, id, event):
        json = self.get(id)
        events = json.get('events', [])
        events.append(event)
        self.collection.find_one_and_update({'_id': id}, {'$set': {'events': events}})

    def get_start_time(self, id):
        try:
            return self.collection.find_one({'_id': id})['events'][0]['timestamp']
        except:
            return None

    def get_end_time(self, id):
        try:
            return self.collection.find_one({'_id': id})['events'][-1]['timestamp']
        except:
            return None
