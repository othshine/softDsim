from django.urls import path

from .views import app, instructor, rest, user

urlpatterns = [
    path('', app.index, name='homepage'),
    path('s/<sid>', app.app, name='app'),
    path('new/<sid>', app.create_new),
    path('result/<sid>', app.result_stats),
    path("login", user.login_request, name="login"),
    path("logout", user.logout_request, name="logout"),
    path("register", user.register_request, name="register"),
    path('continue/<sid>', rest.click_continue, name='continue'),
    path('review/<sid>', instructor.review, name='playback'),
    path('instructor/login', instructor.login, name='instructor'),
    path('instructor/', instructor.instructor_, name='instructor'),
    path('instructor/<sid>', instructor.instructor_inspect),
    path('instructor/<sid>/<username>', instructor.inpect_user),
    path('instructor/search', instructor.instructor_search, name='instructor_search'),
    path('scenarios/', instructor.scenarios),
    path('scenarios/<sid>', instructor.get_scenario),
    path('instructor/search/scenarios', instructor.scenario_search_result),
    path('instructor/add/scenario', instructor.add_scenario),
    path('instructor/edit/<sid>', instructor.edit),
    path('instructor/add/decision/<sid>', instructor.add_decision),
    path('instructor/edit/<sid>/<nr>', instructor.edit_decision),
    path('play/<sid>', rest.play),
    path('createusers', instructor.create_users),
]
