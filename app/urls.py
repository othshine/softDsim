from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='homepage'),
    path('s/<sid>', views.app, name='app'),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    path("register", views.register_request, name="register"),
    path('continue/', views.click_continue, name='continue'),
    path('instructor/', views.instructor, name='instructor'),
    path('instructor/search', views.instructor_search, name='instructor_search'),
    path('scenarios/', views.scenarios),
    path('scenarios/<sid>', views.get_scenario),
    path('instructor/search/scenarios', views.scenario_search_result),
    path('instructor/add/scenario', views.add_scenario),
    path('instructor/edit/<sid>', views.edit),
    path('instructor/add/decision/<sid>', views.add_decision),
    path('instructor/edit/<sid>/<nr>', views.edit_decision)
]
