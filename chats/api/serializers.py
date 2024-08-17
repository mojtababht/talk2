from django.db.models import Count
from rest_framework import serializers

from ..models import Chat, Message


class ProfileSerializer(serializers.Serializer):
    avatar = serializers.ImageField()
    last_online = serializers.DateTimeField()

    class Meta:
        ref_name = 'chat-profile'


class MemberSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    profile = ProfileSerializer()


class ChatSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('id', 'members')


class CreateChatSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Chat
        fields = ('id', 'members', 'user')

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if len(attrs['members']) == 1:
            if (Chat.objects.annotate(members__count=Count('members'))
                    .filter(members=attrs['user'])
                    .filter(members=attrs['members'][0], members__count=2).exists()):
                raise serializers.ValidationError('this chat exists')
        return attrs

    @property
    def validated_data(self):
        validated_data = super().validated_data
        user = validated_data.pop('user')
        validated_data['members'].append(user)
        return validated_data


class UpdateChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ('members', )

    def update(self, instance, validated_data):
        if instance.members.count() == 2:
            raise serializers.ValidationError('regular chat can not change')
        return super().update(instance, validated_data)


class CreateMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Message
        fields = ('id', 'user', 'text', 'created_at_date', 'created_at_time',
                  'updated_at_date', 'updated_at_time')

    @property
    def validated_data(self):
        validated_data = super().validated_data
        validated_data.update({'chat_id': self.context.get('chat_id')})
        return validated_data


class MessageSerializer(serializers.ModelSerializer):
    user = serializers.SlugField()

    class Meta:
        model = Message
        fields = ('id', 'user', 'text', 'created_at_date', 'created_at_time', 'updated_at_date', 'updated_at_time')
