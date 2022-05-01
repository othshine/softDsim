from django.urls import path, include
from .api import endpoint_test, user
from .api.management_goal import TaskGoalViews
from .api.views.scenario_view import ScenarioView
from .api.security.security_view import (
    LoginView,
    GetCSRFToken,
    LogoutView,
    CheckAuthenticatedView,
    SignupView,
)


# all request with /api/ land here (see softDsim/urls.py)
urlpatterns = [
    path("test", endpoint_test.api_test, name="api_test"),
    path("user/count", user.user_count, name="user_count"),
    path("task-goal/", TaskGoalViews.as_view()),
    path("task-goal/<str:id>", TaskGoalViews.as_view()),
    path("scenario/", ScenarioView.as_view(), name="scenario"),
    path("scenario/<str:scenario_id>", ScenarioView.as_view(), name="get_one_scenario"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("csrf_cookie", GetCSRFToken.as_view(), name="csrf_cookie"),
    path("authenticated", CheckAuthenticatedView.as_view(), name="authenticated"),
    path("register", SignupView.as_view(), name="register"),
    path("user/", include("app.api.endpoints.user_endpoint")),
]
