# Generated by Django 4.1.3 on 2022-11-07 10:20

from django.conf import settings
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("round_of_game", models.PositiveIntegerField()),
                ("date", models.DateField()),
            ],
            options={
                "abstract": False,
            },
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
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("first", models.PositiveIntegerField(blank=True, null=True)),
                ("second", models.PositiveIntegerField(blank=True, null=True)),
                ("third", models.PositiveIntegerField(blank=True, null=True)),
                ("fourth", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "bowler",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "date",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="score.regulargamedate",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
