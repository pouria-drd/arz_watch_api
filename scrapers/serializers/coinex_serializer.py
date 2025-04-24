from rest_framework import serializers


class ArzDigitalDataSerializer(serializers.Serializer):
    symbol = serializers.CharField()
    name = serializers.CharField()
    name_fa = serializers.CharField()
    price_usd = serializers.CharField()
    price_irr = serializers.CharField()
    change_24h = serializers.CharField()
    market_cap = serializers.CharField()
    last_update = serializers.CharField()
