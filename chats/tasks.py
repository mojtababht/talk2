from celery import shared_task
from channels.layers import get_channel_layer
import asyncio


@shared_task
def send_notifications(users_id):
    channel_layer = get_channel_layer()

    async def send_for_one_user(user_id):
        user_id = str(user_id)
        await channel_layer.group_send(f'infos_{user_id}', {
            "type": "send_notification",
            'user_id': user_id
        })

    async def send_to_all(users_id):
        await asyncio.gather(*(send_for_one_user(user_id) for user_id in users_id))

    asyncio.run(send_to_all(users_id))
