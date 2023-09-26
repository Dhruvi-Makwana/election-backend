from .views import RegistrationApi, LoginAPIView,UserListApi
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView
)
app_name = "user_api"

urlpatterns = [
    path("register/", RegistrationApi.as_view(), name="register_api"),
    path("login/", LoginAPIView.as_view(), name="login_api"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/", UserListApi.as_view(), name="user_list"),
   ]
