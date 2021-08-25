from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('continue/', views.click_continue, name='continue')
]