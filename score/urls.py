from django.urls import path
from . import views

urlpatterns = [
    path("<int:pk>/", views.RegularGameScores.as_view()),
]
