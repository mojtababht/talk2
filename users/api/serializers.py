from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from ..models import User, Profile


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(validators=(UniqueValidator(queryset=User.objects.all(),
                                                                 message='this username already exists'), ))
    password = serializers.CharField()
    password_repeat = serializers.CharField()
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    first_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not attrs['password'] == attrs['password_repeat']:
            raise serializers.ValidationError('password and password_repeat does not match')
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('avatar', 'is_online', 'last_online')


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile')
