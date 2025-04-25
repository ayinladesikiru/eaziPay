from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers
from .models import Profile


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'phone']


class ProfileSerializer(serializers.ModelSerializer):
    bvn = serializers.CharField(max_length=11, min_length=11)
    class Meta:
        model = Profile
        fields = ['user', 'image', 'address', 'bvn', 'nin']
