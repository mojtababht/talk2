import json

from django.utils.timezone import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from channels.exceptions import DenyConnection

from .serializers import CreateMessageSerializer, MessageSerializer
from ..models import Chat, Message


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.user = self.scope['user']
        self.chat = await self.get_chat(self.chat_id)
        self.room_group_name = "chat_%s" % self.chat_id
        if not self.chat:
            raise DenyConnection()
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.set_user_online()
        await self.accept()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.set_user_offline()
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if message := text_data_json.get("message"):
            await self.channel_layer.group_send(self.room_group_name, {"type": "chat_message", "message": message})

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        data = {'user': self.user.id, 'chat': self.chat.id, 'text': message}
        await self.save_message(data)
        response = await self.get_messages()
        await self.send(text_data=json.dumps(response))

    @database_sync_to_async
    def get_chat(self, chat_id):
        try:
            chat = Chat.objects.get(id=chat_id)
            if not self.user in chat.members.all():
                return False
        except Chat.DoesNotExist:
            return False
        return chat

    @database_sync_to_async
    def get_chat_name(self, chat):
        return chat.name

    @database_sync_to_async
    def set_user_online(self):
        profile = self.user.profile
        profile.is_online = True
        profile.save()

    @database_sync_to_async
    def set_user_offline(self):
        profile = self.user.profile
        profile.is_online = False
        profile.last_online = datetime.now()
        profile.save()

    @database_sync_to_async
    def save_message(self, data):
        serializer = CreateMessageSerializer(data=data)
        serializer.is_valid()
        serializer.save()

    @database_sync_to_async
    def get_messages(self):
        messages = Message.objects.filter(chat=self.chat)
        return MessageSerializer(messages, many=True).data



