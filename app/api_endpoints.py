from django.urls import path

from app.api.views.user_scenario import UserScenarioViews
from app.api.views.team import SkillTypeView, TeamViews, MemberView
from app.api.views.scenario_config import ScenarioConfigView
from .api.views.decision_view import DecisionView
from .api.views.scenario_view import ScenarioView
from .api.views.management_goal_view import ManagementGoalView
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
    # User stuff
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("csrf-cookie", GetCSRFToken.as_view(), name="csrf-cookie"),
    path("authenticated", CheckAuthenticatedView.as_view(), name="authenticated"),
    path("register", RegisterView.as_view(), name="register"),
    path("user", UserView.as_view()),
    path("user/<str:username>", UserView.as_view()),
    # template scenario
    path("template-scenario", TemplateScenarioView.as_view()),
    path("template-scenario/<str:scenario_id>", TemplateScenarioView.as_view()),
    # user scenario
    path("user-scenario", UserScenarioViews.as_view()),
    path("user-scenario/<int:id>", UserScenarioViews.as_view()),
    # this (scenario) is old
    path("scenario/", ScenarioView.as_view(), name="scenario"),
    path("scenario/<str:scenario_id>", ScenarioView.as_view(), name="get_one_scenario"),
    # decision todo: remove maybe later
    path("decision", DecisionView.as_view(), name="decision"),
    path("decision/<str:decision_id>", DecisionView.as_view(), name="decision"),
    path("management-goal/", ManagementGoalView.as_view()),
    path("management-goal/<str:id>", ManagementGoalView.as_view()),
    # team and member
    path("team", TeamViews.as_view()),
    path("team/<int:id>", TeamViews.as_view()),
    path("member", MemberView.as_view()),
    path("member/<int:id>", MemberView.as_view()),
    path("skill-type", SkillTypeView.as_view()),
    path("skill-type/<int:id>", SkillTypeView.as_view()),
    # scenario config
    path("scenario-config", ScenarioConfigView.as_view()),
    path("scenario-config/<str:id>", ScenarioConfigView.as_view()),
]
