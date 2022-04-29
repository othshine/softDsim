from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from app.api.views.user_view import UsersView

urlpatterns = [
    path('', UsersView.as_view()),
    path('<str:username>', UsersView.getOne)
]

urlpatterns = format_suffix_patterns(urlpatterns)