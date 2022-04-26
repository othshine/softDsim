from django.urls import path

from .api import endpoint_test, scenario, user

urlpatterns = [
    path('test', endpoint_test.api_test, name='api_test'),
    path('scenario', scenario.scenario, name="scenario"),
    path('user/count', user.user_count, name="user_count")
]
