from django.urls import path, include

# from users import views
from .api.views import scenario_view
from .api.security.security_view import LoginView, GetCSRFToken, LogoutView, CheckAuthenticatedView, SignupView



# all request with /api/ land here (see softDsim/urls.py)
urlpatterns = [
    path('scenario/', scenario_view.ScenarioEndpoint.scenario, name="scenario"),
    path('scenario/<str:id>', scenario_view.ScenarioEndpoint.get_one_scenario, name="get_one_scenario"),
    path('login', LoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('csrf_cookie', GetCSRFToken.as_view()),
    path('authenticated', CheckAuthenticatedView.as_view()),
    path('register', SignupView.as_view()),
    path('user/', include('app.api.endpoints.user_endpoint')),

]
