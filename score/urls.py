from django.urls import path
from . import views

urlpatterns = [
    path("<int:pk>/", views.RegularGameScores.as_view()),
    path("dates/", views.RegularGameDates.as_view()),
    path("dates/<int:pk>/", views.RegularGameDateDetail.as_view()),
]
