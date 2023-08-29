from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.exceptions import NotFound, ParseError
from .models import User
from .serializers import PublicUserSerializer, PrivateUserSerializer


class Users(APIView):
    def get(self, request):
        all_users = User.objects.all()
        serializer = PublicUserSerializer(all_users, many=True)
        return Response(serializer.data)


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = PrivateUserSerializer(user)
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        serializer = PrivateUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(PrivateUserSerializer(user).data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LogOut(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response()


class PasswordLogIn(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(request=request, username=username, password=password)
        if user:
            login(request, user)
            return Response()
        else:
            return Response({"error": "wrong password"}, status=HTTP_400_BAD_REQUEST)


class KakaoLogIn(APIView):
    pass
