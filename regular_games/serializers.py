from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.exceptions import ParseError
from .models import RegularGameDate, RegularGameScore
from users.models import User
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


class TinyRegularGameScoreSerializer(ModelSerializer):
    rank = SerializerMethodField()
    date = RegularGameDateSerializer()
    participant_count = SerializerMethodField()

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

    def get_participant_count(self, regular_game_score):
        return regular_game_score.date.regulargamescore_set.count()

    class Meta:
        model = RegularGameScore
        fields = (
            "score1",
            "score2",
            "score3",
            "score4",
            "total_score",
            "game_count",
            "average",
            "high_low",
            "rank",
            "participant_count",
            "date",
        )


class MyRecordsSerializer(ModelSerializer):
    first_regular_game_date = SerializerMethodField()
    continuous_days = SerializerMethodField()
    total_regular_game_count = SerializerMethodField()
    total_game_count = SerializerMethodField()
    total_total_score = SerializerMethodField()
    total_average = SerializerMethodField()
    max_score = SerializerMethodField()
    min_score = SerializerMethodField()
    max_rank = SerializerMethodField()
    max_rank_count = SerializerMethodField()
    average_area = SerializerMethodField()
    regular_game_scores = SerializerMethodField()
    participation_rate = SerializerMethodField()

    def get_first_regular_game_date(self, me):
        try:
            first_regular_game = RegularGameScore.objects.filter(bowler=me).earliest()
            return first_regular_game.date.date
        except Exception:
            return ""

    def get_continuous_days(self, me):
        first_regular_game_date = self.get_first_regular_game_date(me)
        if not first_regular_game_date or not me.join_date:
            return ""
        return (first_regular_game_date - me.join_date).days

    def get_total_regular_game_count(self, me):
        try:
            return RegularGameScore.objects.filter(bowler=me).count()
        except Exception:
            return 0

    def get_total_game_count(self, me):
        try:
            all_regular_games = RegularGameScore.objects.filter(bowler=me)
            return sum(regular_game.game_count() for regular_game in all_regular_games)
        except Exception:
            return 0

    def get_total_total_score(self, me):
        try:
            all_regular_games = RegularGameScore.objects.filter(bowler=me)
            return sum(regular_game.total_score() for regular_game in all_regular_games)
        except Exception:
            return 0

    def get_total_average(self, me):
        game_count = self.get_total_game_count(me)
        if not game_count:
            return 0
        return round(self.get_total_total_score(me) / game_count, 2)

    def get_max_score(self, me):
        try:
            all_regular_games = RegularGameScore.objects.filter(bowler=me)
            result = [0]
            for regular_game in all_regular_games:
                result.append(max(regular_game.scores()))
            return max(result)
        except Exception:
            return 0

    def get_min_score(self, me):
        try:
            all_regular_games = RegularGameScore.objects.filter(bowler=me)
            scores = [999]
            for regular_game in all_regular_games:
                for x in regular_game.scores():
                    if x:
                        scores.append(x)
            return min(scores)
        except Exception:
            return 0

    def cal_rank(self, me):
        try:
            all_regular_games = RegularGameScore.objects.filter(bowler=me)
            result = [999]
            for regular_game in all_regular_games:
                rank = 1
                my_average = regular_game.average()
                queryset = regular_game.date.regulargamescore_set.exclude(bowler=me)
                for query in queryset:
                    if query.average() > my_average:
                        rank += 1
                result.append(rank)
            return result
        except Exception:
            return 0

    def get_max_rank(self, me):
        return min(self.cal_rank(me))

    def get_max_rank_count(self, me):
        rank = self.cal_rank(me)
        return rank.count(min(rank))

    def get_average_area(self, me):
        try:
            all_regular_games = RegularGameScore.objects.filter(bowler=me)
            if not all_regular_games:
                return []
            result = [0 for _ in range(31)]
            for regular_game in all_regular_games:
                if regular_game.score1:
                    result[regular_game.score1 // 10] += 1
                if regular_game.score2:
                    result[regular_game.score2 // 10] += 1
                if regular_game.score3:
                    result[regular_game.score3 // 10] += 1
                if regular_game.score4:
                    result[regular_game.score4 // 10] += 1
            return result
        except Exception:
            return []

    def get_regular_game_scores(self, me):
        try:
            all_regular_games = RegularGameScore.objects.filter(bowler=me)
            return TinyRegularGameScoreSerializer(all_regular_games, many=True).data
        except Exception:
            return []

    def get_participation_rate(self, me):
        try:
            if me.join_date:
                return round(
                    (
                        RegularGameScore.objects.filter(
                            bowler=me, date__date__gte=me.join_date
                        ).count()
                        / RegularGameDate.objects.filter(date__gte=me.join_date).count()
                    )
                    * 100
                )
            else:
                return round(
                    (
                        RegularGameScore.objects.filter(bowler=me).count()
                        / RegularGameDate.objects.all().count()
                    )
                    * 100
                )
        except Exception:
            return 0

    class Meta:
        model = User
        fields = (
            "name",
            "avatar",
            "gender",
            "birth_date",
            "join_date",
            "position",
            "first_regular_game_date",  # 첫 정기전 참여일
            "continuous_days",  # 근속년수(일수)
            "total_regular_game_count",  # 정기전 참여 횟수
            "total_game_count",  # 총 게임 횟수
            "total_total_score",  # 총 점수
            "total_average",  # 총 평균
            "max_score",  # 최고 점수
            "min_score",  # 최저 점수
            "max_rank",  # 최고 등수
            "max_rank_count",  # 최고 등수 몇 번?
            "participation_rate",  # 참여율
            "average_area",  # 전체 점수 점수대별 막대 그래프
            "regular_game_scores",
            # 시드 변화 그래프
        )
