from django.contrib.auth import get_user_model, login, authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from ..permissions import CustomPermission
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (UserSerializer, LoginSerializer, StateSerializer, CountrySerializer,
                          CitySerializer, AreaSerializer, AddressSerializer, PoliticalPartySerializer,
                          ElectionSerializer, BoothSerializers, EvmMachineSerializer, VoteSerializer)
from rest_framework import status, viewsets
from user.constants import LOGIN_ERROR_MESSAGE
from user.models import State, Country, City, Area, Address, PoliticalParty, Election, Booth, EVMMachine, Vote
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
    permission_classes = [IsAuthenticated, CustomPermission]
    permissions_required = {"GET": ["user.view_user"], "POST": ["user.add_user"],
                            "PUT": ["user.change_user"], "DELETE": ["user.delete_user"]}


class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [IsAuthenticated, CustomPermission]
    permissions_required = {"GET": ["user.view_state"], "POST": ["user.add_state"],
                            "PUT": ["user.change_state"], "DELETE": ["user.delete_state"]}


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsAuthenticated, CustomPermission]
    permissions_required = {"GET": ["user.view_country"], "POST": ["user.add_country"],
                            "PUT": ["user.change_country"], "DELETE": ["user.delete_country"]}


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated, CustomPermission]
    permissions_required = {"GET": ["user.view_city"], "POST": ["user.add_city"],
                            "PUT": ["user.change_city"], "DELETE": ["user.delete_city"]}


class AreaViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, CustomPermission]
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permissions_required = {"GET": ["user.view_area"], "POST": ["user.add_area"],
                            "PUT": ["user.change_area"], "DELETE": ["user.delete_area"]}


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [CustomPermission]
    permissions_required = {"GET": ["user.view_address"], "POST": ["user.add_address"],
                            "PUT": ["user.change_address"], "DELETE": ["user.delete_address"]}


class PoliticalPartyViewSet(viewsets.ModelViewSet):
    queryset = PoliticalParty.objects.all()
    serializer_class = PoliticalPartySerializer
    permission_classes = [IsAuthenticated, CustomPermission]
    permissions_required = {"GET": ["user.view_politicalparty"], "POST": ["user.add_politicalparty"],
                            "PUT": ["user.change_politicalparty"], "DELETE": ["user.delete_politicalparty"]}


class ElectionViewSet(viewsets.ModelViewSet):
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer
    permission_classes = [IsAuthenticated, CustomPermission]
    permissions_required = {"GET": ["user.view_election"], "POST": ["user.add_election"],
                            "PUT": ["user.change_election"], "DELETE": ["user.delete_election"]}


class BoothViewSet(viewsets.ModelViewSet):
    queryset = Booth.objects.all()
    serializer_class = BoothSerializers
    permission_classes = [IsAuthenticated, CustomPermission]
    permissions_required = {"GET": ["user.view_booth"], "POST": ["user.add_booth"],
                            "PUT": ["user.change_booth"], "DELETE": ["user.delete_booth"]}


class EvmMachineViewSet(viewsets.ModelViewSet):
    queryset = EVMMachine.objects.all()
    serializer_class = EvmMachineSerializer
    permission_classes = [IsAuthenticated, CustomPermission]
    permissions_required = {"GET": ["user.view_evm_machine"], "POST": ["user.add_evm_machine"],
                            "PUT": ["user.change_evm_machine"], "DELETE": ["user.delete_evm_machine"]}


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated, CustomPermission]
    permissions_required = {"GET": ["user.view_vote"], "POST": ["user.add_vote"],
                            "PUT": ["user.change_vote"], "DELETE": ["user.delete_vote"]}
