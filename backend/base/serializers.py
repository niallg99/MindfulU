from rest_framework import serializers
from base.models import (
    Event,
    ScrapedData,
    SupportLink,
    SupportSection,
    Mood,
    MoodCause,
)


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


class SupportSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportSection
        fields = "__all__"


class CustomSupportLinkSerializer(serializers.ModelSerializer):
    section_title = serializers.SerializerMethodField()

    class Meta:
        model = SupportLink
        fields = ("id", "section_title", "link_text", "link_url")

    def get_section_title(self, obj):
        return obj.section.title if obj.section else None


class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = "__all__"


class MoodCauseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodCause
        fields = "__all__"

