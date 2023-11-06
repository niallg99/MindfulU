from rest_framework import serializers
from base.models import Event, ScrapedData, SupportLink, SupportLink


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class ScrapedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapedData
        fields = "__all__"


class SupportLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportLink
        fields = "__all__"
