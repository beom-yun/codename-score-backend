from django.contrib import admin
from .models import RegularGameScore, RegularGameDate


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
