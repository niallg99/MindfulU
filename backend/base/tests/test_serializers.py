from django.test import TestCase
from base.models import Event, ScrapedData, SupportLink, SupportSection, Mood, MoodCause, Friends, UserProfile
from base.serializers import (
    EventSerializer,
    ScrapedDataSerializer,
    SupportLinkSerializer,
    SupportSectionSerializer,
    MoodSerializer,
    MoodCauseSerializer,
    FriendSerializer,
    UserProfileSerializer,
    UserSerializer,
    CustomSupportLinkSerializer,
    FriendRequestSerializer
)
from django.contrib.auth.models import User
from django.utils import timezone

class SerializerTestCase(TestCase):

    def test_event_serializer(self):
        event = Event.objects.create(name='Event Test', date='2023-01-01', duration='1 hour')
        serializer = EventSerializer(event)
        data = serializer.data
        self.assertEqual(data['name'], 'Event Test')

    def test_scraped_data_serializer(self):
        scraped_data = ScrapedData.objects.create(url='http://example.com', title='Example')
        serializer = ScrapedDataSerializer(scraped_data)
        data = serializer.data
        self.assertEqual(data['title'], 'Example')

    def test_support_link_serializer(self):
        section = SupportSection.objects.create(title='Section Test')
        support_link = SupportLink.objects.create(section=section, link_text='Link Test', link_url='http://example.com')
        serializer = SupportLinkSerializer(support_link)
        data = serializer.data
        self.assertEqual(data['link_text'], 'Link Test')

    def test_custom_support_link_serializer(self):
        section = SupportSection.objects.create(title='Section Test')
        support_link = SupportLink.objects.create(section=section, link_text='Link Test', link_url='http://example.com')
        serializer = CustomSupportLinkSerializer(support_link)
        data = serializer.data
        self.assertEqual(data['section_title'], 'Section Test')

    def test_mood_serializer(self):
        user = User.objects.create_user(username='user1', password='pass')
        mood = Mood.objects.create(user=user, mood_type='Happy')
        serializer = MoodSerializer(mood)
        data = serializer.data
        self.assertEqual(data['mood_type'], 'Happy')

    def test_mood_cause_serializer(self):
        mood_cause = MoodCause.objects.create(cause_type='Academic')
        serializer = MoodCauseSerializer(mood_cause)
        data = serializer.data
        self.assertEqual(data['cause_type'], 'Academic')

    def test_user_profile_serializer(self):
        user = User.objects.create_user(username='user1', password='pass')
        user_profile = UserProfile.objects.create(user=user, phone='1234567890')
        serializer = UserProfileSerializer(user_profile)
        data = serializer.data
        self.assertEqual(data['phone'], '1234567890')

    def test_user_serializer(self):
        user = User.objects.create_user(username='user1', password='pass')
        user_profile = UserProfile.objects.create(user=user, phone='1234567890')
        serializer = UserSerializer(user)
        data = serializer.data
        self.assertEqual(data['username'], 'user1')
        self.assertEqual(data['profile']['phone'], '1234567890')

    def test_friend_serializer(self):
        user1 = User.objects.create_user(username='user1', password='pass')
        user2 = User.objects.create_user(username='user2', password='pass')
        friends_instance = Friends.objects.create(user=user1, friend=user2, friendship_status='Accepted')
        serializer = FriendSerializer(friends_instance)
        data = serializer.data
        self.assertEqual(data['user']['username'], 'user1')
        self.assertEqual(data['friend']['username'], 'user2')
        self.assertEqual(data['friendship_status'], 'Accepted')

    def test_friend_request_serializer(self):
        user1 = User.objects.create_user(username='user1', password='pass')
        user2 = User.objects.create_user(username='user2', password='pass')
        friend_request = Friends.objects.create(user=user1, friend=user2, friendship_status='Requested')
        serializer = FriendRequestSerializer(friend_request)
        data = serializer.data
        self.assertEqual(data['sender'], 'user1')
        self.assertEqual(data['status'], 'Requested')
