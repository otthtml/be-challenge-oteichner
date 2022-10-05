from django.db import models

# Create your models here.
class League(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    area = models.CharField(max_length=100)

class Team(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=10)
    area = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    league = models.ManyToManyField(League)

class BasePlayer(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)
    team = models.ManyToManyField(Team)

class Player(BasePlayer):
    position = models.CharField(max_length=100)

class Coach(BasePlayer):
    pass
