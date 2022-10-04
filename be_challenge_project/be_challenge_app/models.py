from django.db import models

# Create your models here.
class League(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    area = models.CharField(max_length=100)
