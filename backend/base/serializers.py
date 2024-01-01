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
		UserProfile,
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

class UserProfileSerializer(serializers.ModelSerializer):
		picture = serializers.ImageField(use_url=True)
		
		class Meta:
				model = UserProfile
				fields = ('user', 'phone', 'streak_count', 'picture')

				
class UserSerializer(serializers.ModelSerializer):
		profile = UserProfileSerializer()  # Nested serializer for UserProfile
		class Meta:
				model = User
				fields = ('id', 'username', 'first_name', 'last_name', 'email', 'profile')

		def get_streak_count(self, obj):
				return obj.profile.calculate_streak_count() if obj.profile else 0


class FriendSerializer(serializers.ModelSerializer):
		user = UserSerializer()
		friend = UserSerializer()
		most_recent_mood = serializers.SerializerMethodField()
		show_mood = serializers.SerializerMethodField()

		class Meta:
				model = Friends
				fields = ('id', 'user', 'friend', 'friendship_status', 'created_at', 'updated_at', 'most_recent_mood', 'show_mood')

		def get_most_recent_mood(self, obj):
				last_mood = Mood.objects.filter(user=obj.friend).order_by('-mood_date').first()
				if last_mood:
						return f"{last_mood.mood_type} on {last_mood.mood_date.strftime('%Y-%m-%d')}"
				return None

		def get_show_mood(self, obj):
				try:
						user_profile = UserProfile.objects.get(user=obj.friend)
						return user_profile.show_mood
				except UserProfile.DoesNotExist:
						return False



class FriendRequestSerializer(serializers.ModelSerializer):
		sender = serializers.CharField(source='user.username')
		username = serializers.CharField(source='user.username')
		status = serializers.CharField(source='friendship_status')

		class Meta:
				model = Friends
				fields = ('id', 'sender', 'username', 'status')