from uuid import uuid4

from django.db import models
from django.conf import settings


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chats')

    class Meta:
        ordering = ('-messages__created_at_date', '-messages__created_at_time')


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.CharField(max_length=256)
    created_at_date = models.DateField(auto_now_add=True)
    created_at_time = models.TimeField(auto_now_add=True)
    updated_at_date = models.DateField(auto_now=True)
    updated_at_time = models.TimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at_date', '-created_at_time')
