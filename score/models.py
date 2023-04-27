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

    def score_list(self):
        return [x for x in (self.first, self.second, self.third, self.fourth) if x]

    def total_score(self):
        return sum(self.score_list())

    def game_count(self):
        return len(self.score_list())

    def max_score(self):
        return max(self.score_list())

    def min_score(self):
        return min(self.score_list())

    def average(self):
        return self.total_score() / self.game_count()


class RegularGameDate(CommonModel):
    round_of_game = models.PositiveIntegerField()
    date = models.DateField()

    def __str__(self):
        return str(self.date)
