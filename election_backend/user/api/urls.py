from .views import (RegistrationApi, LoginAPIView,UserListApi, StateViewSet, CountryViewSet,
                    CityViewSet, AreaViewSet, AddressViewSet, PoliticalPartyViewSet, ElectionViewSet,
                    BoothViewSet, EvmMachineViewSet, VoteViewSet)

from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView
)
from django.urls import path, include

app_name = "user_api"
router = SimpleRouter()
router.register("state", StateViewSet, basename="state")
router.register("country", CountryViewSet, basename="country")
router.register("city", CityViewSet, basename="city")
router.register("area", AreaViewSet, basename="area")
router.register("address", AddressViewSet, basename="address")
router.register("political-party", PoliticalPartyViewSet, basename="political_party")
router.register("elections", ElectionViewSet, basename="election")
router.register("booth", BoothViewSet, basename="booth")
router.register("evm-machine", EvmMachineViewSet, basename="evm_machine")
router.register("vote", VoteViewSet, basename="vote")

urlpatterns = [
    path("register/", RegistrationApi.as_view(), name="register_api"),
    path("login/", LoginAPIView.as_view(), name="login_api"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/", UserListApi.as_view(), name="user_list"),
    path('', include(router.urls)),
   ]
