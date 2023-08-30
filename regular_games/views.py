from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
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
