from rest_framework import serializers


class TGJUDataSerializer(serializers.Serializer):
    title = serializers.CharField()
    price = serializers.CharField()
    change_percentage = serializers.CharField()
    change_amount = serializers.CharField()
    last_update = serializers.DateTimeField()
