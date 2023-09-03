import requests
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
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
    def post(self, request):
        try:
            code = request.data.get("code")
            access_token = requests.post(
                "https://kauth.kakao.com/oauth/token",
                headers={
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
                },
                data={
                    "grant_type": "authorization_code",
                    "client_id": "06acaa0ad678eefcbb78902fec710ad6",
                    "redirect_uri": "http://127.0.0.1:3000/social/kakao/",
                    "code": code,
                },
            ).json()
            access_token = access_token.get("access_token")
            user_data = requests.get(
                "https://kapi.kakao.com/v2/user/me",
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
                },
            ).json()
            kakao_account = user_data.get("kakao_account")
            profile = kakao_account.get("profile")
            try:
                user = User.objects.get(email=kakao_account.get("email"))
                login(request, user)
                return Response(status=HTTP_200_OK)
            except User.DoesNotExist:
                user = User.objects.create(
                    email=kakao_account.get("email"),
                    username=profile.get("nickname"),
                    name=profile.get("nickname"),
                    gender=kakao_account.get("gender"),
                    avatar=profile.get("profile_image_url"),
                )
                user.set_unusable_password()
                user.save()
                login(request, user)
                return Response(status=HTTP_200_OK)
        except Exception:
            return Response(status=HTTP_400_BAD_REQUEST)
