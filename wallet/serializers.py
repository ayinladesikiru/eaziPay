from rest_framework import serializers


class FundSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=1000, max_value=10000000)
