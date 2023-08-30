from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ParseError
from .models import RegularGameDate, RegularGameScore
from users.serializers import PublicUserSerializer


class RegularGameDateSerializer(ModelSerializer):
    class Meta:
        model = RegularGameDate
        fields = "__all__"

    def validate_round_of_game(self, value):
        if RegularGameDate.objects.filter(round_of_game=value).exists():
            raise ParseError(f"해당 회차({value})가 이미 존재합니다.")
        return value


class RegularGameScoreSerializer(ModelSerializer):
    bowler = PublicUserSerializer(read_only=True)

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
        )
