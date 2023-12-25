from django.test import TestCase
from django.contrib.auth.models import User
from base.models import UserProfile, MoodCause, Mood, Friends, ScrapedData, Event, SupportSection, SupportLink, BroadcastMessage
from django.core.files.uploadedfile import SimpleUploadedFile

class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('john', 'john@example.com', 'johnpassword')
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            phone='123456789',
            streak_count=10,
            show_mood=True
        )

    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile.user.username, 'john')
        self.assertEqual(self.user_profile.phone, '123456789')
        self.assertEqual(self.user_profile.streak_count, 10)
        self.assertTrue(self.user_profile.show_mood)

class MoodCauseTest(TestCase):
    def test_mood_cause_creation(self):
        mood_cause = MoodCause.objects.create(cause_type='Academic')
        self.assertEqual(str(mood_cause), 'Academic')

class MoodTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('jane', 'jane@example.com', 'janepassword')
        self.mood = Mood.objects.create(
            user=self.user,
            mood_type='Happy',
            description='Feeling great!'
        )

    def test_mood_creation(self):
        self.assertEqual(str(self.mood), f'{self.user.username} - Happy on {self.mood.mood_date}')

class FriendsTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user('alice', 'alice@example.com', 'alicepassword')
        self.user2 = User.objects.create_user('bob', 'bob@example.com', 'bobpassword')
        self.friendship = Friends.objects.create(
            user=self.user1,
            friend=self.user2,
            friendship_status='Accepted'
        )

    def test_friends_creation(self):
        self.assertEqual(str(self.friendship), f'{self.user1.username} and {self.user2.username} - Status: Accepted')

class ScrapedDataTest(TestCase):
    def test_scraped_data_creation(self):
        scraped_data = ScrapedData.objects.create(
            url='http://example.com',
            title='Test Title',
            description='Test Description',
            scraped_content='Test Content'
        )
        self.assertEqual(str(scraped_data), 'Test Title')

class EventTest(TestCase):
    def test_event_creation(self):
        event = Event.objects.create(name='Test Event')
        self.assertEqual(str(event), 'Test Event')

class SupportSectionTest(TestCase):
    def test_support_section_creation(self):
        support_section = SupportSection.objects.create(title='Test Support Section')
        self.assertEqual(str(support_section), 'Test Support Section')

class SupportLinkTest(TestCase):
    def setUp(self):
        self.support_section = SupportSection.objects.create(title='Test Support Section')
        self.support_link = SupportLink.objects.create(
            section=self.support_section,
            link_text='Test Link Text',
            link_url='http://example.com'
        )

    def test_support_link_creation(self):
        self.assertEqual(self.support_link.link_text, 'Test Link Text')
        self.assertEqual(self.support_link.link_url, 'http://example.com')

class BroadcastMessageTest(TestCase):
    def test_broadcast_message_creation(self):
        message = BroadcastMessage.objects.create(message='Test Message')
        self.assertTrue('Broadcast Message created at' in str(message))
