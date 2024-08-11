from uuid import uuid4

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    ...


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, unique=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True)
    last_online = models.DateTimeField()
