from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "남")
        FEMALE = ("female", "여")

    class PositionChoices(models.TextChoices):
        CHAIRMAN = ("chairman", "회장")
        EXECUTIVE = ("executive", "운영진")
        GENERAL = ("general", "일반회원")

    first_name = models.CharField(max_length=150, editable=False)
    last_name = models.CharField(max_length=150, editable=False)
    name = models.CharField(max_length=150, verbose_name="이름")
    avatar = models.URLField(null=True, blank=True)
    gender = models.CharField(
        max_length=10, choices=GenderChoices.choices, verbose_name="성별"
    )
    birth_date = models.DateField(null=True, blank=True, verbose_name="생년월일")
    join_date = models.DateField(null=True, blank=True, verbose_name="가입일")
    position = models.CharField(
        max_length=10,
        choices=PositionChoices.choices,
        default=PositionChoices.GENERAL,
        verbose_name="직책",
    )
    # phone_number
