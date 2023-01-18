from django.urls import path
from . import views

urlpatterns = [
    path("", views.Bowlers.as_view()),
    path("me/", views.Me.as_view()),
    path("change-password/", views.ChangePassword.as_view()),
    path("login/", views.Login.as_view()),
    path("logout/", views.Logout.as_view()),
]
