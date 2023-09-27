from datetime import date
from django.contrib.auth import get_user_model
from rest_framework import serializers
from user.constants import PASSWORD_ERROR_MESSAGE, BIRTH_DATE_ERROR
from django.contrib.auth.hashers import make_password
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', "username", "nationality", "date_of_birth", "living_from",
                  "profile", "confirm_password"]

    def validate_date_of_birth(self, value):
        if value < date(1910, 1, 1):
            raise serializers.ValidationError(BIRTH_DATE_ERROR)
        return value

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")
        if not password == confirm_password:
            raise serializers.ValidationError(PASSWORD_ERROR_MESSAGE)
        attrs.pop("confirm_password", None)
        attrs["password"] = make_password(password)
        return attrs


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
