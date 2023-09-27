from django.contrib.auth.models import AbstractUser
from django.db import models
from django_extensions.db.models import TimeStampedModel


class State(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=20, unique=True)
    flag = models.ImageField(upload_to="flags/")
    state = models.ManyToManyField(State)

    class Meta:
        verbose_name_plural = 'countries'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=20)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="cities")

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=20)
    pincode = models.CharField(max_length=6)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="areas")

    def __str__(self):
        return self.name


class Address(models.Model):
    street_name = models.CharField(max_length=200, null=True)
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="address")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="get_address")

    def __str__(self):
        return self.street_name


class User(AbstractUser):
    nationality = models.ForeignKey(Country, blank=True, null=True, on_delete=models.CASCADE, related_name="citizen")
    date_of_birth = models.DateField(null=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE,related_name="users", null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="user", null=True)
    living_from = models.DateField(null=True)
    profile = models.ImageField(upload_to="profile/", null=True)

    def __str__(self):
        return self.username


class PoliticalParty(models.Model):
    symbol = models.ImageField(upload_to="political_party_symbol/")
    name = models.CharField(max_length=20)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="political_parties")
    chairman = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chairman")

    def __str__(self):
        return self.name


class Election(TimeStampedModel):
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="election_countries")
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name="election_states")
    political_parties = models.ManyToManyField(PoliticalParty)
    opening_date = models.DateField()
    closing_date = models.DateField()

    def __str__(self):
        return self.name


class Booth(TimeStampedModel):
    name = models.CharField(max_length=100)
    belong_to = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="booths")

    def __str__(self):
        return self.name


class EVMMachine(TimeStampedModel):
    belong_to = models.ManyToManyField(Booth, related_name="machines")

    def __str__(self):
        return self.belong_to.name


class Vote(TimeStampedModel):
    machine = models.ForeignKey(EVMMachine, on_delete=models.CASCADE, related_name="votes")
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="voter")
    vote = models.BooleanField(default=False)

    def __str__(self):
        return self.voter.username
