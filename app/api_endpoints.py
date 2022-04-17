from django.urls import path

from .api import endpoint_test

urlpatterns = [
    path('test', endpoint_test.api_test, name='api_test'),
]
