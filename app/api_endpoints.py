from django.urls import path, include

from .api.views.scenario_view import ScenarioView
from .api.security.security_view import (
    LoginView,
    GetCSRFToken,
    LogoutView,
    CheckAuthenticatedView,
    SignupView,
)

from app.api.views.team import SkillTypeView, TeamViews, MemberView
from app.api.views.scenario_config import ScenarioConfigView

# all request with /api/ land here (see softDsim/urls.py)
urlpatterns = [
    path("scenario/", ScenarioView.as_view(), name="scenario"),
    path("scenario/<str:scenario_id>", ScenarioView.as_view(), name="get_one_scenario"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("csrf-cookie", GetCSRFToken.as_view(), name="csrf-cookie"),
    path("authenticated", CheckAuthenticatedView.as_view(), name="authenticated"),
    path("register", SignupView.as_view(), name="register"),
    path("user/", include("app.endpoints.user_endpoint")),
    path("team", TeamViews.as_view()),
    path("team/<int:id>", TeamViews.as_view()),
    path("member", MemberView.as_view()),
    path("member/<int:id>", MemberView.as_view()),
    path("skill-type", SkillTypeView.as_view()),
    path("skill-type/<int:id>", SkillTypeView.as_view()),
    path("scenario-config", ScenarioConfigView.as_view()),
    path("scenario-config/<str:id>", ScenarioConfigView.as_view()),
]
