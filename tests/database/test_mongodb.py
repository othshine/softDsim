import pytest

from utils import get_db_handle


@pytest.mark.django_db
def test_mongo_can_save_document():
    db, client = get_db_handle('test', 'localhost', 2717)
    post = {"info": "test result", "a": "b"}
    posts = db.posts
    posts.insert_one(post)

    assert posts.find_one({"info": "test result"})["a"] == "b"
