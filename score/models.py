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
        return f"{self.date.round_of_game} / {self.bowler.username}"

    def total_score(self):
        return self.first + self.second + self.third + self.fourth

    def average(self):
        count = (
            (1 if self.first else 0)
            + (1 if self.second else 0)
            + (1 if self.third else 0)
            + (1 if self.fourth else 0)
        )
        return self.total_score() / count


class RegularGameDate(CommonModel):
    round_of_game = models.PositiveIntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.date} ({self.round_of_game}회차)"
