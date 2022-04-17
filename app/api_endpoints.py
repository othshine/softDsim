from django.urls import path

from .api import test_endpoint

urlpatterns = [
    path('test', test_endpoint.api_test, name='api_test'),
]
