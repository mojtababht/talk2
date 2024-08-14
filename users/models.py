from uuid import uuid4

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status


class CustomUserManager(UserManager):
    ...


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, unique=True)

    objects = CustomUserManager()

    @classmethod
    def login(cls, username, password):
        if user := cls.objects.filter(username=username):
            user = user.get()
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return {"access": str(refresh.access_token), "refresh": str(refresh)}
        raise AuthenticationFailed()

    @classmethod
    def signup(cls, data):
        password = data.pop('password')
        user = cls(**data)
        user.set_password(password)
        user.save()
        return 'ok', status.HTTP_201_CREATED  # TODO: fix actual response

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True)
    is_online = models.BooleanField(default=False)
    last_online = models.DateTimeField()
