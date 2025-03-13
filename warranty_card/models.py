from django.contrib.auth.models import AbstractUser
from django.db import models
import random

class User(AbstractUser):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    unique_code = models.IntegerField(unique=True, blank=True, null=True)

    def __str__(self):
        return f"{self.name} {self.surname}"
