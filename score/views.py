from rest_framework.views import APIView
from rest_framework.response import Response
from .models import RegularGameScore, RegularGameDate
from .serializers import RegularGameSerializer


class RegularGameScores(APIView):
    def get(self, request, pk):
        scores = RegularGameScore.objects.filter(date__pk=pk)
        serializer = RegularGameSerializer(scores, many=True)
        return Response(serializer.data)
