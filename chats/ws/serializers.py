from django.conf import settings
from rest_framework import serializers

from ..models import Message, Chat
from reusable.utils import decrypt_message


class ProfileSerializer(serializers.Serializer):
    last_online = serializers.DateTimeField()
    is_online = serializers.BooleanField()

    class Meta:
        ref_name = 'ws-chat-profile'


class MemberSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    profile = ProfileSerializer()


class CreateMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('user', 'chat', 'text')


class MessageSerializer(serializers.ModelSerializer):
    user = MemberSerializer(read_only=True)
    created_at_time = serializers.TimeField(read_only=True, format='%H:%M')
    text = serializers.SerializerMethodField()

    def get_text(self, obj):
        return decrypt_message(obj.text, obj.chat.id)

    class Meta:
        model = Message
        fields = ('id', 'user', 'text', 'created_at_date', 'created_at_time', 'updated_at_date', 'updated_at_time')


class ChatNotifSerializer(serializers.ModelSerializer):
    unread_messages = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ('id', 'name', 'avatar', 'members', 'unread_messages')

    def get_name(self, obj):
        if obj.name:
            name = obj.name
        else:
            other = obj.members.exclude(id=self.context['user_id']).first()
            if other.first_name:
                name = other.first_name
            else:
                name = other.username
        return name

    def get_avatar(self, obj):
        if obj.avatar:
            avatar = obj.avatar
        elif obj.members.count() == 2:
            avatar = obj.members.exclude(id=self.context['user_id']).first().profile.avatar
        else:
            avatar = ''
        if avatar:
            if request := self.context.get("request"):
                return request.build_absolute_uri(avatar.url)
            return settings.BASE_URL + avatar.url
        return None

    def get_members(self, obj):
        members = obj.members.exclude(id=self.context['user_id']).all()
        return MemberSerializer(members, many=True, context=self.context).data

    def get_unread_messages(self, obj):
        user_id = self.context['user_id']
        query = obj.messages.exclude(seen_by__id=user_id).all()
        return MessageSerializer(query, many=True, context=self.context).data
