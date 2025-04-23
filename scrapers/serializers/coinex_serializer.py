from rest_framework import serializers


class CoinexDataSerializer(serializers.Serializer):
    symbol = serializers.CharField()
    name = serializers.CharField()
    name_fa = serializers.CharField()
    price_usd = serializers.CharField()
    change_24h = serializers.CharField()
    market_cap = serializers.CharField()
    volume_24h = serializers.CharField()
