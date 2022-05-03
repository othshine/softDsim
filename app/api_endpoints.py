from django.urls import path, include

from .api.views.scenario_view import ScenarioView

from .api.views.management_goal_view import TaskGoalView, ManagementGoalView
from .api.security.security_view import (
    LoginView,
    GetCSRFToken,
    LogoutView,
    CheckAuthenticatedView,
    RegisterView,
)


# all request with /api/ land here (see softDsim/urls.py)
from .api.views.template_scenario_view import TemplateScenarioView
from .api.views.user_view import UserView

urlpatterns = [
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("csrf-cookie", GetCSRFToken.as_view(), name="csrf-cookie"),
    path("authenticated", CheckAuthenticatedView.as_view(), name="authenticated"),
    path("register", RegisterView.as_view(), name="register"),
    path("user", UserView.as_view()),
    path("user/<str:username>", UserView.as_view()),
    path("template_scenario", TemplateScenarioView.as_view()),
    path("template_scenario/<str:scenario_id>", TemplateScenarioView.as_view()),
    # for testing
    path("task-goal/", TaskGoalView.as_view()),
    path("task-goal/<str:id>", TaskGoalView.as_view()),
    path("management-goal/", ManagementGoalView.as_view()),
    path("management-goal/<str:id>", ManagementGoalView.as_view()),
    # this (scenario) is old
    path("scenario/", ScenarioView.as_view(), name="scenario"),
    path("scenario/<str:scenario_id>", ScenarioView.as_view(), name="get_one_scenario"),
]
