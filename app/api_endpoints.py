from django.urls import path

from .api import endpoint_test, scenario, user
from .api.management_goal import TaskGoalViews

urlpatterns = [
    path("test", endpoint_test.api_test, name="api_test"),
    path("scenario", scenario.scenario, name="scenario"),
    path("user/count", user.user_count, name="user_count"),
    path("login", user.login, name="login"),
    path("logged", user.auth, name="test_login"),
    path("task-goal/", TaskGoalViews.as_view()),
    path("task-goal/<str:id>", TaskGoalViews.as_view()),
]
