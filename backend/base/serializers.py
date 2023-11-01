from rest_framework import serializers
from base.models import Event, ScrapedData

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class ScrapedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapedData
        fields = '__all__'
