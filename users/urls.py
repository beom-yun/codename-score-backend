from django.urls import path
from .views import Me, Users, PasswordLogIn, LogOut

urlpatterns = [
    path("", Users.as_view()),
    path("me/", Me.as_view()),
    path("log-in/", PasswordLogIn.as_view()),
    path("log-out/", LogOut.as_view()),
]
