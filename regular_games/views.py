from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from .models import RegularGameDate, RegularGameScore
from .serializers import RegularGameDateSerializer, RegularGameScoreSerializer
from users.models import User


class RegularGameDates(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        all_regular_game_dates = RegularGameDate.objects.all()
        serializer = RegularGameDateSerializer(all_regular_game_dates, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RegularGameDateSerializer(data=request.data)
        if serializer.is_valid():
            new_regular_game_date = serializer.save()
            serializer = RegularGameDateSerializer(new_regular_game_date)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class RegularGameDateDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return RegularGameDate.objects.get(pk=pk)
        except RegularGameDate.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        regular_game_date = self.get_object(pk)
        return Response(RegularGameDateSerializer(regular_game_date).data)

    def put(self, request, pk):
        regular_game_date = self.get_object(pk)
        serializer = RegularGameDateSerializer(
            regular_game_date, data=request.data, partial=True
        )
        if serializer.is_valid():
            updated_regular_game_date = serializer.save()
            return Response(RegularGameDateSerializer(updated_regular_game_date).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        regular_game_date = self.get_object(pk)
        regular_game_date.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RegularGameScores(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return RegularGameDate.objects.get(pk=pk)
        except RegularGameDate.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        regular_game_date = self.get_object(pk)
        scores = regular_game_date.regulargamescore_set.all()
        return Response(RegularGameScoreSerializer(scores, many=True).data)


class RegularGameScoreDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_date(self, date_pk):
        try:
            return RegularGameDate.objects.get(pk=date_pk)
        except RegularGameDate.DoesNotExist:
            raise NotFound("회차정보 없음")

    def get_user(self, user_pk):
        try:
            return User.objects.get(pk=user_pk)
        except User.DoesNotExist:
            raise NotFound("유저 찾기 불가")

    def get_object(self, date_pk, user_pk):
        try:
            return RegularGameScore.objects.get(
                date=self.get_date(date_pk), bowler=self.get_user(user_pk)
            )
        except RegularGameScore.DoesNotExist:
            raise NotFound

    def get(self, request, date_pk, user_pk):
        score = self.get_object(date_pk, user_pk)
        return Response(RegularGameScoreSerializer(score).data)

    def post(self, request, date_pk, user_pk):
        regular_game_date = self.get_date(date_pk)
        bowler = self.get_user(user_pk)
        if RegularGameScore.objects.filter(
            date=regular_game_date, bowler=bowler
        ).exists():
            raise ParseError(f"해당 인원({bowler})의 해당 회차({regular_game_date}) 정보가 존재합니다.")
        serializer = RegularGameScoreSerializer(data=request.data)
        if serializer.is_valid():
            new_regular_game_score = serializer.save(
                date=regular_game_date, bowler=bowler
            )
            return Response(RegularGameScoreSerializer(new_regular_game_score).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def put(self, request, date_pk, user_pk):
        score = self.get_object(date_pk, user_pk)
        serializer = RegularGameScoreSerializer(score, data=request.data, partial=True)
        if serializer.is_valid():
            updated_score = serializer.save()
            return Response(RegularGameScoreSerializer(updated_score).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, date_pk, user_pk):
        score = self.get_object(date_pk, user_pk)
        score.delete()
        return Response(status=HTTP_204_NO_CONTENT)
