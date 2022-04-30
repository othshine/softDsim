from django.urls import path, include

# from users import views
from .api.views import scenario_view
from .api.security.security_view import LoginView, GetCSRFToken, LogoutView, CheckAuthenticatedView, SignupView



# all request with /api/ land here (see softDsim/urls.py)
urlpatterns = [
    path('scenario/', scenario_view.ScenarioEndpoint.scenario, name="scenario"),
    path('scenario/<str:id>', scenario_view.ScenarioEndpoint.get_one_scenario, name="get_one_scenario"),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('csrf_cookie', GetCSRFToken.as_view(), name='csrf_cookie'),
    path('authenticated', CheckAuthenticatedView.as_view(), name='authenticated'),
    path('register', SignupView.as_view(), name='register'),
    path('user/', include('app.api.endpoints.user_endpoint')),

]
