from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("profile_list", views.profile_list, name="profile_list"),
    path("profile/<int:pk>", views.profile, name="profile"),
    path("profile/followers/<int:pk>", views.followers, name="followers"),
    path("profile/following/<int:pk>", views.following, name="following"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register_user/", views.register_user, name="register_user"),
    path("update_user/", views.update_user, name="update_user"),
    path("feek_like/<int:pk>", views.feek_like, name="feek_like"),
    path("feek_show/<int:pk>", views.feek_show, name="feek_show"),
    path("unfollow/<int:pk>", views.unfollow, name="unfollow"),
    path("follow/<int:pk>", views.follow, name="follow"),
    path("delete_feek/<int:pk>", views.delete_feek, name="delete_feek"),
    path("edit_feek/<int:pk>", views.edit_feek, name="edit_feek"),
    path("search/", views.search_feek, name="search_feek"),
]
