from django.contrib import admin
from .models import User, State, Country, Area, Election, City, Booth, EVMMachine, Vote, Address


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "nationality", "city"]


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ["id", "street_name", "area", "country"]


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "flag"]


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "pincode", "city"]


@admin.register(Election)
class ElectionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "country", "state"]


@admin.register(Booth)
class BoothAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "belong_to"]


@admin.register(EVMMachine)
class EVMMachineAdmin(admin.ModelAdmin):
    list_display = ["id"]


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ["id", "machine", "voter", "vote"]
