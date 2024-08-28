from .models import Event
from rest_framework import serializers


class EventSerializer(serializers.Serializer):
    date = serializers.DateField()
    views = serializers.IntegerField()
    clicks = serializers.IntegerField()
    cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    cpc = serializers.SerializerMethodField()
    cpm = serializers.SerializerMethodField()

    def get_cpc(self, obj):
        if obj['clicks'] == 0:
            return 0
        return round(obj['cost'] / obj['clicks'], 2)

    def get_cpm(self, obj):
        if obj['views'] == 0:
            return 0
        return round((obj['cost'] / obj['views']) * 1000, 2)

    def create(self, validated_data):
        return Event.objects.create(**validated_data)
