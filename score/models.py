from django.db import models
from common.models import CommonModel


class RegularGameScore(CommonModel):
    first = models.PositiveIntegerField(default=0)
    second = models.PositiveIntegerField(default=0)
    third = models.PositiveIntegerField(default=0)
    fourth = models.PositiveIntegerField(default=0)
    date = models.ForeignKey("score.RegularGameDate", on_delete=models.CASCADE)
    bowler = models.ForeignKey("users.User", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date.round_of_game}회차 / {self.bowler.name}"

    def total_score(self):
        return self.first + self.second + self.third + self.fourth

    def game_count(self):
        return (
            (1 if self.first else 0)
            + (1 if self.second else 0)
            + (1 if self.third else 0)
            + (1 if self.fourth else 0)
        )

    def average(self):
        return self.total_score() / self.game_count()


class RegularGameDate(CommonModel):
    round_of_game = models.PositiveIntegerField()
    date = models.DateField()

    def __str__(self):
        return str(self.date)


# class SeedRecord(CommonModel):
#     class SeedChoices(models.IntegerChoices):
#         FIRST_SEED = 1
#         SECOND_SEED = 2
#         THIRD_SEED = 3
#         FOURTH_SEED = 4
#         FIFTH_SEED = 5
#         SIXTH_SEED = 6

#     month = models.DateField()
#     bowler = models.ForeignKey("users.User", on_delete=models.CASCADE)
#     seed = models.IntegerField(choices=SeedChoices.choices)

#     def aver_of_month(self):
#         month_score = RegularGameScore.objects.filter(
#             bowler=self.bowler,
#             date__date__year=self.month.year,
#             date__date__month=self.month.month,
#         )
#         month_total_game_count = 0
#         month_total_score = 0
#         for score in month_score:
#             month_total_game_count += score.game_count()
#             month_total_score += score.total_score()
#         return round(month_total_score / month_total_game_count, 2)

#     def __str__(self):
#         return f"{self.bowler} / {self.seed}"
