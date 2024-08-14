from rest_framework import serializers

from ..models import Message


class CreateMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ('user', 'chat', 'text')


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.SlugField()

    class Meta:
        model = Message
        fields = ('id', 'user', 'text', 'created_at_date', 'created_at_time', 'updated_at_date', 'updated_at_time')
