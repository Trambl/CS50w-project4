from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("submit_post", views.submit_post, name="submit_post"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following/<str:username>", views.following_users, name="following"),
    path("edit_post", views.edit_post, name="edit_post"),
    path("like_post", views.like_post, name="like_post"),
]
