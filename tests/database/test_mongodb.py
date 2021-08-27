import pytest

from app.src.domain.decision_tree import Scenario
from mongo_models import ScenarioMongoModel, NoObjectWithIdException
from utils import get_db_handle




@pytest.mark.django_db
def test_mongo_can_save_document():
    db, client = get_db_handle('test', 'localhost', 2717)
    post = {"info": "test result", "a": "b"}
    posts = db.posts
    posts.insert_one(post)

    assert posts.find_one({"info": "test result"})["a"] == "b"


def test_mongo_scenario_can_be_saved_loaded_and_deleted():
    mongo = ScenarioMongoModel()
    s = Scenario(budget=100000, scheduled_days=40, tasks=300)
    s2 = Scenario(budget=215, scheduled_days=677, tasks=2, current_day=30, actual_cost=300000, counter=4)

    mid = mongo.save(s)
    result = mongo.get(mid)
    assert result == s

    mid2 = mongo.save(s2)
    result2 = mongo.get(mid2)
    assert result2 == s2

    mongo.remove(obj=s)
    with pytest.raises(NoObjectWithIdException):
        mongo.get(mid)

    mid2 = mongo.save(s2)
    result2 = mongo.get(mid2)
    assert result2 == s2

    mongo.remove(mid=mid2)
    with pytest.raises(NoObjectWithIdException):
        mongo.get(mid)
    









