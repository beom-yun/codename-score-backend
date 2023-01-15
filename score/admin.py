import csv
from django.contrib import admin
from .models import RegularGameScore, RegularGameDate


@admin.action(description="Download a csv file")
def download_regulargame_csv(model_admin, request, queryset):
    f = open("output.csv", "w", encoding="utf-8", newline="")
    wr = csv.writer(f)
    wr.writerow(["date", "name", "first", "second", "third", "fourth"])
    for scores in queryset:
        wr.writerow(
            [
                scores.date,
                scores.bowler.name,
                scores.first,
                scores.second,
                scores.third,
                scores.fourth,
            ]
        )
    f.close()


@admin.action(description="Upload a csv file")
def upload_regulargame_csv(model_admin, request, queryset):
    print("Upload regular game scores")


@admin.register(RegularGameScore)
class RegularGameScoreAdmin(admin.ModelAdmin):
    actions = (
        download_regulargame_csv,
        upload_regulargame_csv,
    )

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
