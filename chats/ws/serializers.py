from rest_framework import serializers

from ..models import Message
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
