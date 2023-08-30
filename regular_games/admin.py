from django.contrib import admin
from .models import RegularGameDate, RegularGameScore, RegularGameSeed


@admin.register(RegularGameDate)
class RegularGameDateAdmin(admin.ModelAdmin):
    list_display = (
        "round_of_game",
        "date",
    )


@admin.register(RegularGameScore)
class RegularGameScoreAdmin(admin.ModelAdmin):
    list_display = (
        "bowler",
        "date",
        "score1",
        "score2",
        "score3",
        "score4",
        "total_score",
        "game_count",
        "average",
    )

    list_filter = (
        "date__round_of_game",
        "bowler",
    )


@admin.register(RegularGameSeed)
class RegularGameSeedAdmin(admin.ModelAdmin):
    list_display = (
        "bowler",
        "month",
        "seed",
    )
