from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import RegularGameScore, RegularGameDate
from .serializers import RegularGameSerializer, RegularGameDateSerializer


class RegularGameDates(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        dates = RegularGameDate.objects.all()
        serializer = RegularGameDateSerializer(dates, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RegularGameDateSerializer(data=request.data)
        if serializer.is_valid():
            round_of_game = request.data.get("round_of_game")
            date = request.data.get("date")
            if RegularGameDate.objects.filter(round_of_game=round_of_game).exists():
                raise ParseError("이미 존재하는 회차입니다.")
            if RegularGameDate.objects.filter(date=date).exists():
                raise ParseError("이미 정기전이 진행된 날짜입니다.")
            regular_game_date = serializer.save()
            return Response(RegularGameDateSerializer(regular_game_date).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class RegularGameDateDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return RegularGameDate.objects.get(pk=pk)
        except RegularGameDate.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        regular_game_date = self.get_object(pk)
        serializer = RegularGameDateSerializer(regular_game_date)
        return Response(serializer.data)

    def put(self, request, pk):
        regular_game_date = self.get_object(pk)
        serializer = RegularGameDateSerializer(
            regular_game_date, data=request.data, partial=True
        )
        if serializer.is_valid():
            round_of_game = request.data.get("round_of_game")
            date = request.data.get("date")
            if (
                round_of_game
                and RegularGameDate.objects.filter(round_of_game=round_of_game).exists()
            ):
                raise ParseError("이미 존재하는 회차입니다.")
            if date and RegularGameDate.objects.filter(date=date).exists():
                raise ParseError("이미 정기전이 진행된 날짜입니다.")
            updated_regular_game_date = serializer.save()
            return Response(RegularGameDateSerializer(updated_regular_game_date).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        regular_game_date = self.get_object(pk)
        regular_game_date.delete()
        return Response(status=HTTP_204_NO_CONTENT)


class RegularGameScores(APIView):
    def get(self, request, pk):
        scores = RegularGameScore.objects.filter(date__pk=pk)
        serializer = RegularGameSerializer(scores, many=True)
        return Response(serializer.data)
