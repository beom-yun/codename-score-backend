from django.urls import path
from .views import RegularGameDates

urlpatterns = [
    path("", RegularGameDates.as_view()),
]
