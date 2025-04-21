from rest_framework import serializers


class TGJUDataSerializer(serializers.Serializer):
    title = serializers.CharField()
    price = serializers.CharField()
    changePercentage = serializers.CharField(source="change_percentage")
    changeAmount = serializers.CharField(source="change_amount")
    lastUpdate = serializers.DateTimeField(source="last_update")
