from django.contrib import admin
from .models import RegularGameScore, RegularGameDate, SeedRecord


@admin.register(RegularGameScore)
class RegularGameScoreAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "date",
        "bowler",
        "first",
        "second",
        "third",
        "fourth",
        "total_score",
        "average",
    )


@admin.register(RegularGameDate)
class RegularGameDateAdmin(admin.ModelAdmin):
    pass


@admin.register(SeedRecord)
class SeedRecordAdmin(admin.ModelAdmin):
    list_display = (
        "month",
        "bowler",
        "seed",
        "aver_of_month",
    )
