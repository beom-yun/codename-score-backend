from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.status import HTTP_400_BAD_REQUEST
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

    def delete(self, request):
        pass


class RegularGameScores(APIView):
    def get(self, request, pk):
        scores = RegularGameScore.objects.filter(date__pk=pk)
        serializer = RegularGameSerializer(scores, many=True)
        return Response(serializer.data)
