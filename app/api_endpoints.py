from django.urls import path

from .api import endpoint_test, scenario


# all request with /api land here (see softDsim/urls.py)
urlpatterns = [
    path('test', endpoint_test.api_test, name='api_test'),
    path('scenario/', scenario.scenario, name="scenario"),
    path('scenario/<str:id>', scenario.get_one_scenario, name="get_one_scenario")

]
