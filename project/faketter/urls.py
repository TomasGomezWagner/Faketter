from django.urls import path

from . import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("profile_list", views.profile_list, name="profile_list"),
    path("profile/<int:pk>", views.profile, name="profile"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register_user/", views.register_user, name="register_user"),
    path("update_user/", views.update_user, name="update_user"),
    path("feek_like/<int:pk>", views.feek_like, name="feek_like"),
    path("feek_show/<int:pk>", views.feek_show, name="feek_show"),
]
