from celery import shared_task
from channels.layers import get_channel_layer



@shared_task
def send_notif(users):
    channel_layer = get_channel_layer()
    for user in users:
        channel_layer.send(f"infos{user.id}", {
            "type": "send_notification",
            'chats': user.chats.prefetch_related('members', 'messages').all(),
        })
