from django.db import models

# Create your models here.
class Superusers(models.Model):
    username = models.CharField(max_length=60)
    password = models.CharField(max_length=50)
    confirm_password = models.CharField(max_length=50)
    name = models.CharField(max_length=60)
    speciality = models.CharField(max_length=60)
    organization = models.CharField(max_length=60)
