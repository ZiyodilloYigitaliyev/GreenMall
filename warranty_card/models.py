from django.contrib.auth.models import AbstractUser
from django.db import models
import random

class User(AbstractUser):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    password = models.CharField(max_length=255)
    unique_code = models.IntegerField(unique=True, blank=True, null=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="warranty_card_users",
        blank=True
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="warranty_card_users_permissions",
        blank=True
    )

    def save(self, *args, **kwargs):
        if not self.unique_code:
            self.unique_code = random.randint(100000, 999999)
        super().save(*args, **kwargs)
