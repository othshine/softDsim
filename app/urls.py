from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('continue/', views.click_continue, name='continue'),
    path('instructor/', views.instructor, name='instructor'),
    path('instructor/search', views.instructor_search, name='instructor_search'),
    path('scenarios/', views.scenarios),
    path('scenarios/<sid>', views.get_scenario),
    path('instructor/search/scenarios', views.scenario_search_result),
    path('instructor/add/scenario', views.add_scenario),
    path('instructor/edit/<sid>', views.edit)
]