from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class RegularGameDate(models.Model):
    """정기전 날짜 모델"""

    round_of_game = models.PositiveIntegerField(verbose_name="회차")
    date = models.DateField(verbose_name="정기전 날짜")

    def __str__(self):
        return f"{self.date} ({self.round_of_game}회차)"


class RegularGameScore(models.Model):
    """정기전 점수 모델"""

    bowler = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, verbose_name="볼러"
    )
    date = models.ForeignKey(
        "regular_games.RegularGameDate",
        on_delete=models.CASCADE,
        verbose_name="정기전 날짜",
    )
    score1 = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(300), MinValueValidator(0)],
        verbose_name="1게임",
    )
    score2 = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(300), MinValueValidator(0)],
        verbose_name="2게임",
    )
    score3 = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(300), MinValueValidator(0)],
        verbose_name="3게임",
    )
    score4 = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MaxValueValidator(300), MinValueValidator(0)],
        verbose_name="4게임",
    )

    def scores(self):
        return (
            self.score1 if self.score1 else 0,
            self.score2 if self.score2 else 0,
            self.score3 if self.score3 else 0,
            self.score4 if self.score4 else 0,
        )

    def total_score(self):
        return sum(self.scores())

    def game_count(self):
        return 4 - self.scores().count(0)

    def average(self):
        if not self.game_count():
            return 0
        return round(self.total_score() / self.game_count(), 2)


# class RegularGameSeed(models.Model):
#     pass
