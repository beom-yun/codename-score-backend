from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.exceptions import ParseError
from .models import RegularGameDate, RegularGameScore
from users.serializers import PublicUserSerializer


class RegularGameDateSerializer(ModelSerializer):
    class Meta:
        model = RegularGameDate
        fields = (
            "id",
            "round_of_game",
            "date",
            "num_of_bowlers",
        )

    def validate_round_of_game(self, value):
        if RegularGameDate.objects.filter(round_of_game=value).exists():
            raise ParseError(f"해당 회차({value})가 이미 존재합니다.")
        return value


class RegularGameScoreSerializer(ModelSerializer):
    bowler = PublicUserSerializer(read_only=True)
    prev_total_score = SerializerMethodField()
    prev_average = SerializerMethodField()
    rank = SerializerMethodField()

    def get_prev_total_score(self, regular_game_score):
        try:
            return (
                regular_game_score.bowler.regulargamescore_set.filter(
                    date__date__lt=regular_game_score.date.date
                )
                .latest()
                .total_score()
            )
        except Exception:
            return 0

    def get_prev_average(self, regular_game_score):
        try:
            return (
                regular_game_score.bowler.regulargamescore_set.filter(
                    date__date__lt=regular_game_score.date.date
                )
                .latest()
                .average()
            )
        except Exception:
            return 0

    def get_rank(self, regular_game_score):
        rank = 1
        my_average = regular_game_score.average()
        queryset = regular_game_score.date.regulargamescore_set.exclude(
            bowler=regular_game_score.bowler
        )
        for query in queryset:
            if query.average() > my_average:
                rank += 1
        return rank

    class Meta:
        model = RegularGameScore
        fields = (
            "bowler",
            "score1",
            "score2",
            "score3",
            "score4",
            "total_score",
            "game_count",
            "average",
            "high_low",
            "prev_total_score",
            "prev_average",
            "rank",
        )
