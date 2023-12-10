from rest_framework import serializers
from django.contrib.auth.models import User
from base.models import (
    Event,
    ScrapedData,
    SupportLink,
    SupportSection,
    Mood,
    MoodCause,
    Friends,
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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class FriendSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    friend = UserSerializer()
    most_recent_mood = serializers.SerializerMethodField()

    class Meta:
        model = Friends
        fields = ('id', 'user', 'friend', 'friendship_status', 'created_at', 'updated_at', 'most_recent_mood')

    def get_most_recent_mood(self, obj):
        last_mood = Mood.objects.filter(user=obj.friend).order_by('-mood_date').first()
        if last_mood:
            # Format the mood as a string. You can customize this format as needed.
            return f"{last_mood.mood_type} on {last_mood.mood_date.strftime('%Y-%m-%d')}"
        return None


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='user.username')
    username = serializers.CharField(source='user.username')
    status = serializers.CharField(source='friendship_status')

    class Meta:
        model = Friends
        fields = ('id', 'sender', 'username', 'status')