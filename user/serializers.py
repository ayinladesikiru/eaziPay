from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers

from wallet.models import Transaction
from .models import Profile, User


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'phone']


class ProfileSerializer(serializers.ModelSerializer):
    bvn = serializers.CharField(max_length=11, min_length=11)
    class Meta:
        model = Profile
        fields = ['user', 'image', 'address', 'bvn', 'nin']


class WalletSerializer(serializers.Serializer):
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    account_number = serializers.CharField(max_length=10)

class TransactionSerializer(serializers.Serializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class DashBoardSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer()
    sender = TransactionSerializer(many=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'phone', 'wallet', 'sender']

