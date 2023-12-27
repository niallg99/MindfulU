from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from base.models import UserProfile, Mood, Friends, BroadcastMessage
from rest_framework_simplejwt.tokens import RefreshToken

class ViewTestCase(APITestCase):
		def setUp(self):
				self.client = APIClient()
				self.user = User.objects.create_user(username='testuser', password='testpassword', email='testuser@example.com')
				self.user_profile = UserProfile.objects.create(user=self.user, phone='123456789', streak_count=10)
				self.mood = Mood.objects.create(user=self.user, mood_type='Happy')
				self.friend = User.objects.create_user(username='frienduser', password='friendpassword')
				self.friends = Friends.objects.create(user=self.user, friend=self.friend, friendship_status='Accepted')
				self.broadcast_message = BroadcastMessage.objects.create(message='Test Broadcast Message')

				refresh = RefreshToken.for_user(self.user)
				self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

		def test_register_view(self):
				url = reverse('register')
				data = {
						'username': 'newuser',
						'password': 'newpassword',
						'email': 'newuser@example.com',
						'first_name': 'New',
						'last_name': 'User',
						'phone': '1234567890'
				}
				response = self.client.post(url, data)
				self.assertEqual(response.status_code, status.HTTP_201_CREATED)
				self.assertTrue(User.objects.filter(username='newuser').exists())

		def test_login_view(self):
				url = reverse('login')
				data = {
						'username': 'testuser',
						'password': 'testpassword'
				}
				response = self.client.post(url, data)
				self.assertEqual(response.status_code, status.HTTP_200_OK)
				self.assertIn('access_token', response.data)

		def test_get_user_profile_view(self):
				url = reverse('get-user-profile', kwargs={'username': self.user.username})
				response = self.client.get(url)
				self.assertEqual(response.status_code, status.HTTP_200_OK)
				self.assertEqual(response.data['phone'], self.user_profile.phone)

		def test_get_events_view(self):
				url = reverse('get-events')
				response = self.client.get(url)
				self.assertEqual(response.status_code, status.HTTP_200_OK)

class UserViewTests(APITestCase):
		def setUp(self):
				# Create a user for the purpose of authentication
				self.user = User.objects.create_user(username='testuser', password='testpassword')
				self.client = APIClient()
				self.token = RefreshToken.for_user(self.user)
				self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')

		def test_check_staff_status(self):
				url = reverse('check-staff-status')
				response = self.client.get(url)
				self.assertEqual(response.status_code, status.HTTP_200_OK)
				self.assertFalse(response.data['is_staff'])

		def test_verify_user_details(self):
			url = reverse('verify-user-details')
			data = {'email': self.user.email}
			response = self.client.post(url, data)
			self.assertEqual(response.status_code, status.HTTP_200_OK)


		def test_reset_password(self):
			
			url = reverse('reset-password')
			data = {'email': self.user.email, 'new_password': 'newtestpassword'}
			response = self.client.post(url, data)
			self.assertEqual(response.status_code, status.HTTP_200_OK)

		def test_get_events(self):
			url = reverse('get-events')  # Use hyphens instead of underscores
			response = self.client.get(url)
			self.assertEqual(response.status_code, status.HTTP_200_OK)

		def test_get_scraped_data(self):
				url = reverse('get-scraped-data')  # Use hyphens instead of underscores
				response = self.client.get(url)
				self.assertEqual(response.status_code, status.HTTP_200_OK)

		def test_get_mood_choices(self):
				url = reverse('mood-choices')  # Use hyphens instead of underscores
				response = self.client.get(url)
				self.assertEqual(response.status_code, status.HTTP_200_OK)

		def test_get_support_links(self):
				url = reverse('custom-support-links')  # Correct name from urlpatterns
				response = self.client.get(url)
				self.assertEqual(response.status_code, status.HTTP_200_OK)

		def test_post_mood(self):
				url = reverse('post-mood')
				data = {'mood_type': 'Happy', 'description': 'Feeling great!'}  # Ensure 'Happy' is a valid choice
				response = self.client.post(url, data)
				self.assertEqual(response.status_code, status.HTTP_201_CREATED)


		def test_update_mood(self):
				mood = Mood.objects.create(user=self.user, mood_type='Sad')
				url = reverse('update-mood', args=[mood.id])
				data = {'mood_type': 'Happy'}
				response = self.client.patch(url, data)
				self.assertEqual(response.status_code, status.HTTP_200_OK)
				mood.refresh_from_db()
				self.assertEqual(mood.mood_type, 'Happy')

		def test_delete_mood(self):
				mood = Mood.objects.create(user=self.user, mood_type='Sad')
				url = reverse('delete-mood', args=[mood.id])
				response = self.client.delete(url)
				self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
				self.assertFalse(Mood.objects.filter(id=mood.id).exists())

def test_register_view_with_existing_username(self):
		url = reverse('register')
		data = {
				'username': 'testuser',
				'password': 'newpassword',
				'email': 'newuser@example.com',
				'first_name': 'New',
				'last_name': 'User',
				'phone': '1234567890'
		}
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

def test_reset_password_for_nonexistent_user(self):
		url = reverse('reset-password')
		data = {
				'email': 'nonexistent@example.com',
				'new_password': 'newtestpassword'
		}
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

def test_protected_view_unauthorized_access(self):
		self.client.credentials()
		url = reverse('protected-view')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

def test_update_user_profile_with_invalid_data(self):
		url = reverse('update-user-profile', kwargs={'username': self.user.username})
		data = {'phone': 'invalidphone'}
		response = self.client.patch(url, data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

def test_send_friend_request_to_nonexistent_user(self):
		url = reverse('send-friend_request', kwargs={'username': 'nonexistentuser'})
		response = self.client.post(url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

def test_accept_nonexistent_friend_request(self):
		url = reverse('accept-friend_request', kwargs={'username': 'nonexistentuser'})
		response = self.client.post(url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

def test_reject_nonexistent_friend_request(self):
		url = reverse('reject-friend-request', kwargs={'username': 'nonexistentuser'})
		response = self.client.post(url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

def test_remove_non_friend(self):
		non_friend_user = User.objects.create_user(username='nonfriend', password='nonfriendpassword')
		url = reverse('remove-friend', kwargs={'username': non_friend_user.username})
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

def test_post_invalid_mood(self):
		url = reverse('post-mood')
		data = {'mood_type': 'InvalidMood'}
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

def test_get_mood_statistics(self):
		url = reverse('mood-statistics')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

def test_save_broadcast_message_as_non_admin(self):
		self.client.credentials()  # Reset credentials to remove admin privileges
		url = reverse('save-broadcast-message')
		data = {'message': 'New Broadcast Message'}
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

def test_get_latest_broadcast_message_none_exist(self):
		BroadcastMessage.objects.all().delete()
		url = reverse('get-latest-broadcast-message')
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['message'], '')

def test_get_users_with_edge_case_search_parameters(self):
		url = reverse('get-users')
		response = self.client.get(url, {'search': '" OR ""="'})
		self.assertEqual(response.status_code, status.HTTP_200_OK)

def test_update_show_mood_preference(self):
		url = reverse('update-show-mood-preference')
		data = {'showMood': True}
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.user_profile.refresh_from_db()
		self.assertTrue(self.user_profile.show_mood)
