from django.urls import path
from .views import RegularGameDates, RegularGameDateDetail

urlpatterns = [
    path("", RegularGameDates.as_view()),
    path("<int:pk>/", RegularGameDateDetail.as_view()),
]
