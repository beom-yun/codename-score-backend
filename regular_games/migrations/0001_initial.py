# Generated by Django 4.2.4 on 2023-08-29 03:28

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="RegularGameDate",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("round_of_game", models.PositiveIntegerField(verbose_name="회차")),
                ("date", models.DateField(verbose_name="정기전 날짜")),
            ],
        ),
        migrations.CreateModel(
            name="RegularGameScore",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "score1",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MaxValueValidator(300),
                            django.core.validators.MinValueValidator(0),
                        ],
                        verbose_name="1게임",
                    ),
                ),
                (
                    "score2",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MaxValueValidator(300),
                            django.core.validators.MinValueValidator(0),
                        ],
                        verbose_name="2게임",
                    ),
                ),
                (
                    "score3",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MaxValueValidator(300),
                            django.core.validators.MinValueValidator(0),
                        ],
                        verbose_name="3게임",
                    ),
                ),
                (
                    "score4",
                    models.PositiveSmallIntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MaxValueValidator(300),
                            django.core.validators.MinValueValidator(0),
                        ],
                        verbose_name="4게임",
                    ),
                ),
                (
                    "bowler",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="볼러",
                    ),
                ),
                (
                    "date",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="regular_games.regulargamedate",
                        verbose_name="정기전 날짜",
                    ),
                ),
            ],
        ),
    ]
