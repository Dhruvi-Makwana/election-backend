from django.contrib.auth import get_user_model, login, authenticate
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer, LoginSerializer
from user.constants import LOGIN_ERROR_MESSAGE
User = get_user_model()


class RegistrationApi(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.none()
    serializer_class = UserSerializer


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid()
        user = authenticate(request=request, **serializer.validated_data)
        if not user:
            raise ValidationError(LOGIN_ERROR_MESSAGE)
        login(request, user)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh token": str(refresh),
                "access token": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


class UserListApi(ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
