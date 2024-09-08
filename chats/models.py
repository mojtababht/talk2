from uuid import uuid4

from django.db import models
from django.db.models import OuterRef, Subquery, Max
from django.conf import settings

from .tasks import send_notifications


class ChatManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            last_message=Subquery(
                Message.objects.filter(chat=OuterRef('pk')).order_by('-created_at').values_list(
                    'created_at')[:1]
            )
        ).order_by('-last_message')

class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chats')

    objects = ChatManager()



class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages')
    text = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    seen_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='seen_messages')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        id_list = list(self.chat.members.values_list('id', flat=True))
        send_notifications.apply_async(args=(id_list,))

    class Meta:
        ordering = ('-created_at',)
