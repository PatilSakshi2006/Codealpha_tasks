from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("search/", views.search_users, name="search_users"),
    path("<str:username>/", views.profile_view, name="profile"),
    path("<str:username>/follow/", views.toggle_follow, name="toggle_follow"),
]
