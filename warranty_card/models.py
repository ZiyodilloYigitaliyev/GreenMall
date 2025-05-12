from django.contrib.auth.models import AbstractUser
from django.db import models


class Admin(AbstractUser):
    phone = models.CharField(max_length=20, unique=True)
    address = models.TextField()

    def __str__(self):
        return self.username

class User(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, unique=True)
    address = models.TextField()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["name", "surname", "address"]

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = f"{self.name}{self.surname}".replace(" ", "").lower()
        super().save(*args, **kwargs)


