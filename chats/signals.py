import asyncio

from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from django.dispatch import receiver

from .models import Message
from .tasks import send_notif


@receiver(post_save, sender=Message)
def send_notification_on_save(sender, instance, created, **kwargs):
        channel_layer = get_channel_layer()
        async def mmd(user_id):
            await channel_layer.group_send(f'infos{user_id}', {
                "type": "send_notification",
                "message": f"A new object of type {sender.__name__} was saved!"  # Customize message
            })

        send_notif(list(instance.chat.members.values_list('id', flat=True)), mmd)

