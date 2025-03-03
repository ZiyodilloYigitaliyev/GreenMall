from django.contrib.auth.models import AbstractUser
from django.db import models
import random

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    password = models.CharField(max_length=255)
    unique_code = models.IntegerField(unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email  # ✅ `username`ni email bilan to‘ldirish
        if not self.unique_code:
            self.unique_code = random.randint(100000, 999999)  # ✅ 6 xonali kod
        super().save(*args, **kwargs)
