from datetime import date
from django.contrib.auth import get_user_model
from rest_framework import serializers
from user.constants import PASSWORD_ERROR_MESSAGE, BIRTH_DATE_ERROR
from django.contrib.auth.hashers import make_password
from user.models import (State, Country, City, Area, Address, PoliticalParty,Election, Booth, EVMMachine,
                         Vote)
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


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    get_state = StateSerializer(source="state", read_only=True, many=True)

    class Meta:
        model = Country
        fields = ["id", "name", "flag", "state", "get_state"]


class CitySerializer(serializers.ModelSerializer):
    get_state = StateSerializer(source="state", read_only=True)

    class Meta:
        model = City
        fields = ["id", "name", "state", "get_state"]


class AreaSerializer(serializers.ModelSerializer):
    get_cities = CitySerializer(source="city", read_only=True)

    class Meta:
        model = Area
        fields = ["id", "name", "pincode", "city", "get_cities"]


class AddressSerializer(serializers.ModelSerializer):
    get_area = AreaSerializer(source="area", read_only=True)
    get_country = CountrySerializer(source="country", read_only=True)

    class Meta:
        model = Address
        fields = ["id", "street_name", "area", "country", "get_area", "get_country"]


class PoliticalPartySerializer(serializers.ModelSerializer):
    chairman_details = UserSerializer(source="chairman", read_only=True)
    country_details = CountrySerializer(source="country", read_only=True)

    class Meta:
        model = PoliticalParty
        fields = ["id", "symbol", "name", "country", "chairman", "chairman_details", "country_details"]


class ElectionSerializer(serializers.ModelSerializer):
    election_countries = CountrySerializer(source="country", read_only=True)
    election_state = StateSerializer(source="state", read_only=True)

    class Meta:
        model = Election
        fields = ["id", "name", "country", "state", "political_parties", "opening_date", "closing_date",
                  "election_countries", "election_state"]


class BoothSerializers(serializers.ModelSerializer):
    belong_to_area = AreaSerializer(source="belong_to", read_only=True)

    class Meta:
        model = Booth
        fields = ["id", "belong_to", "belong_to_area"]


class EvmMachineSerializer(serializers.ModelSerializer):
    booths = BoothSerializers(source="belong_to", read_only=True, many=True)

    class Meta:
        model = EVMMachine
        fields = ["id", "belong_to", "booths"]


class VoteSerializer(serializers.ModelSerializer):
    machine_name = EvmMachineSerializer(source="machine", read_only=True)
    voter_details = UserSerializer(source="voter", read_only=True)

    class Meta:
        model = Vote
        fields = ["id", "machine", "voter", "vote", "machine_name", "voter_details"]
