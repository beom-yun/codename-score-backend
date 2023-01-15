from rest_framework.views import APIView
from rest_framework.response import Response
from .models import RegularGameScore, RegularGameDate
from .serializers import RegularGameSerializer, RegularGameDateSerializer


class RegularGameDates(APIView):
    def get(self, request):
        dates = RegularGameDate.objects.all()
        serializer = RegularGameDateSerializer(dates, many=True)
        return Response(serializer.data)


class RegularGameScores(APIView):
    def get(self, request, pk):
        scores = RegularGameScore.objects.filter(date__pk=pk)
        serializer = RegularGameSerializer(scores, many=True)
        return Response(serializer.data)
