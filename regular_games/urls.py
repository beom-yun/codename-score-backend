from django.urls import path
from .views import (
    RegularGameDates,
    RegularGameDateDetail,
    RegularGameScores,
    RegularGameScoreDetail,
)

urlpatterns = [
    path("", RegularGameDates.as_view()),
    path("<int:pk>/", RegularGameDateDetail.as_view()),
    path("<int:pk>/scores/", RegularGameScores.as_view()),
    path("<int:date_pk>/scores/<int:user_pk>/", RegularGameScoreDetail.as_view()),
]
