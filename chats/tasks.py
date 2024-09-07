from celery import shared_task
from channels.layers import get_channel_layer
import asyncio
from asgiref.sync import async_to_sync


@shared_task
def send_notif(users_id, func):
    for user_id in users_id:
        user_id = str(user_id)
        asyncio.run(func(user_id))
