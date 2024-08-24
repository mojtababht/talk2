from django.db.models import Count
from django.contrib.auth import get_user_model
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
    name = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ('id', 'name', 'avatar', 'members')

    def get_name(self, obj):
        if obj.name:
            name = obj.name
        else:
            other = obj.members.exclude(id=self.context['request'].user.id).first()
            if other.first_name:
                name = other.first_name
            else:
                name = other.username
        return name

    def get_avatar(self, obj):
        if obj.avatar:
            avatar = obj.avatar
        else:
            avatar = obj.members.exclude(id=self.context['request'].user.id).first().profile.avatar
        if avatar:
            if request := self.context["request"]:
                return request.build_absolute_uri(avatar.url)
            return avatar
        return None

    def get_members(self, obj):
        members = obj.members.exclude(id=self.context['request'].user.id).first()
        return MemberSerializer(members, many=True, context=self.context).data


class CreateChatSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    members = serializers.SlugRelatedField(many=True, queryset=get_user_model().objects.all(), slug_field='username')

    class Meta:
        model = Chat
        fields = ('id', 'members', 'user', 'name', 'avatar')

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
        validated_data['members'] = list(set(validated_data['members']))
        if len(validated_data['members']) == 2:
            validated_data.pop('name', None)
            validated_data.pop('avatar', None)
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
