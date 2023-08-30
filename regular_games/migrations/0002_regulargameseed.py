# Generated by Django 4.2.4 on 2023-08-30 07:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("regular_games", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="RegularGameSeed",
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
                ("month", models.DateField()),
                (
                    "seed",
                    models.CharField(
                        choices=[
                            ("1", "1시드"),
                            ("2", "2시드"),
                            ("3", "3시드"),
                            ("4", "4시드"),
                            ("5", "5시드"),
                            ("6", "6시드"),
                        ],
                        max_length=2,
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
            ],
        ),
    ]
