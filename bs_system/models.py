from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Test(models.Model):
    name =models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    class Meta:
        db_table = "test"