from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class RegularGameDate(models.Model):
    """정기전 날짜 모델"""

    round_of_game = models.PositiveIntegerField(verbose_name="회차")
    date = models.DateField(verbose_name="정기전 날짜")

    def num_of_bowlers(self):
        return self.regulargamescore_set.count()

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

    def high_low(self):
        return max(self.scores()) - min(x for x in self.scores() if x)

    def __str__(self):
        return f"{self.bowler} / {self.date} / {self.average()}"

    class Meta:
        get_latest_by = "date__date"


class RegularGameSeed(models.Model):
    """정기전 시드 모델"""

    class SeedChoices(models.TextChoices):
        SEED_1 = ("1", "1시드")
        SEED_2 = ("2", "2시드")
        SEED_3 = ("3", "3시드")
        SEED_4 = ("4", "4시드")
        SEED_5 = ("5", "5시드")
        SEED_6 = ("6", "6시드")

    bowler = models.ForeignKey(
        "users.User", on_delete=models.SET_NULL, null=True, verbose_name="볼러"
    )
    month = models.DateField()
    seed = models.CharField(max_length=2, choices=SeedChoices.choices)
