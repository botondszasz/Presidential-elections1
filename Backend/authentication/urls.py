from django.contrib import admin
from django.urls import path
from . import views
from . import user
from . import user_information
from . import user_actions

urlpatterns = [
    path('home', views.home, name="home"),
    path('register', user.register, name="register"),
    path('login', user.login, name="login"),
    path('logout', user.logout, name="logout"),
    path('profile', views.profile, name="profile"),
    path('candidates', views.candidates, name="candidates"),
    path("update_profile/<int:user_id>/", user_information.update_profile, name="update_profile"),
    path('update_description', views.update_description, name='update_description'),
    path('user_candidate', views.user_candidate, name="user_candidate"),
    path("apply/<int:user_id>/", user_actions.apply, name="apply"),
    path('admin/', admin.site.urls),
    path('show_leaderboard', views.show_leaderboard, name="show_leaderboard"),
    path('main_page', views.main_page, name="main_page"),
    path('list_candidates', views.list_candidates, name="list_candidates"),
    path("view_profile/<int:pk>", user_actions.view_profile, name="view_profile"),
    path("vote/<int:pk>", user_actions.vote, name="vote"),
    path("hide_candidates", views.hide_candidates, name="hide_candidates"),
    path("remove_vote", user_actions.remove_vote, name="remove_vote"),
    path("remove_application", user_actions.remove_application, name="remove_application"),
    path("social", views.social, name="social"),
    path("submit_socials", user_actions.submit_socials, name="submit_socials"),
    path("winner", views.winner, name="winner"),
]

