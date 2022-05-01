from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from app.api.views.user_view import UserView

urlpatterns = [path("", UserView.as_view()), path("<str:username>", UserView.as_view())]

urlpatterns = format_suffix_patterns(urlpatterns)
