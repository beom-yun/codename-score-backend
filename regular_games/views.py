from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from .models import RegularGameDate
from .serializers import RegularGameDateSerializer


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

    def get(self, request):
        pass

    def put(self, request):
        pass

    def delete(self, request):
        pass
