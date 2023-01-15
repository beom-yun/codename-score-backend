from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import RegularGameScore, RegularGameDate
from users.serializers import BowlerSerializer


class RegularGameDateSerializer(ModelSerializer):
    class Meta:
        model = RegularGameDate
        fields = (
            "round_of_game",
            "date",
        )


class RegularGameSerializer(ModelSerializer):

    # date = RegularGameDateSerializer(read_only=True)
    bowler = BowlerSerializer(read_only=True)
    total_score = SerializerMethodField()
    game_count = SerializerMethodField()
    average = SerializerMethodField()
    last_average = SerializerMethodField()
    average_change = SerializerMethodField()
    high_low = SerializerMethodField()

    class Meta:
        model = RegularGameScore
        fields = (
            # "date",
            "bowler",
            "first",
            "second",
            "third",
            "fourth",
            "total_score",
            "game_count",
            "average",
            "last_average",
            "average_change",
            "high_low",
        )

    def get_total_score(self, regular_game):
        return regular_game.total_score()

    def get_game_count(self, regular_game):
        return regular_game.game_count()

    def get_average(self, regular_game):
        return round(regular_game.average(), 1)

    def get_last_average(self, regular_game):
        try:
            last_average = (
                regular_game.bowler.regulargamescore_set.filter(
                    date__lt=regular_game.date
                )
                .last()
                .average()
            )
            return round(last_average, 1)
        except:
            return 0

    def get_average_change(self, regular_game):
        return round(
            self.get_average(regular_game) - self.get_last_average(regular_game), 1
        )

    def get_high_low(self, regular_game):
        return regular_game.max_score() - regular_game.min_score()
