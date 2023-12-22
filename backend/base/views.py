import logging
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage
from rest_framework import status
from django.db.models import Count
from django.utils import timezone
from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser
from base.models import Event, ScrapedData, Mood, SupportLink, MoodCause, Friends, BroadcastMessage, ProfileInfo, UserProfile, UserProfile
from base.serializers import (
		EventSerializer,
		ScrapedDataSerializer,
		SupportLinkSerializer,
		CustomSupportLinkSerializer,
		MoodSerializer,
		FriendSerializer,
		FriendRequestSerializer,
		UserProfileSerializer,
)

#logging
logger = logging.getLogger(__name__)

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")
    phone = request.data.get("phone", None)  # Get phone number from request

    # Validation logic
    if not all([username, password, email, first_name, last_name]):
        return Response(
            {"success": False, "message": "All fields are required!"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"success": False, "message": "Username already exists!"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # User creation
    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )

    # Saving phone number in UserProfile
    if phone:
        UserProfile.objects.create(user=user, phone=phone)

    return Response(
        {"success": True, "message": "User registered successfully!"},
        status=status.HTTP_201_CREATED
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_staff_status(request):
		"""
		View to check if the currently logged-in user is a staff member.
		"""
		return Response({'is_staff': request.user.is_staff})

@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
		username = request.data.get("username")
		password = request.data.get("password")

		if not username or not password:
				return Response(
						{"error": "All fields are required!"}, status=status.HTTP_400_BAD_REQUEST
				)

		user = authenticate(username=username, password=password)

		if user:
				refresh = RefreshToken.for_user(user)
				response_data = {
						"message": "Login successful!",
						"access_token": str(refresh.access_token),
				}
				return Response(response_data, status=status.HTTP_200_OK)
		else:
				return Response(
						{"error": "Invalid credentials!"}, status=status.HTTP_401_UNAUTHORIZED
				)

@api_view()
@permission_classes([IsAuthenticated])
def protected_view(request):
		return Response({"message": "connected !"}, 200)

@api_view(["POST"])
@permission_classes([AllowAny])
def verify_user_details(request):
		email = request.data.get("email")

		if not email:
				return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

		try:
				user_exists = User.objects.filter(email=email).exists()
				return Response({"verified": user_exists})
		except Exception as e:
				return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["POST"])
@permission_classes([AllowAny])
def reset_password(request):
		email = request.data.get("email")
		new_password = request.data.get("new_password")

		if not email or not new_password:
				return Response({"error": "Email and new password are required"}, status=status.HTTP_400_BAD_REQUEST)

		try:
				user = User.objects.get(email=email)
				user.set_password(new_password)
				user.save()
				return Response({"message": "Password reset successfully."})
		except User.DoesNotExist:
				return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
		except Exception as e:
				return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
def get_events(request):
		events = Event.objects.all()
		serializer = EventSerializer(events, many=True)
		return Response(serializer.data)

@api_view(["GET"])
def get_scraped_data(request):
		scraped_data = ScrapedData.objects.all()
		serializer = ScrapedDataSerializer(scraped_data, many=True)
		return Response(serializer.data)

@api_view(["GET"])
def get_mood_choices(request):
		return Response(Mood.MOOD_CHOICES)

@api_view(["GET"])
def get_support_links(request):
		support_links = SupportLink.objects.all()
		serializer = SupportLinkSerializer(support_links, many=True)

		response = Response(serializer.data)

		return response

@api_view(["GET"])
def get_support_links_view(request):
		support_links = SupportLink.objects.all()
		serializer = CustomSupportLinkSerializer(support_links, many=True)

		support_data = {}
		for item in serializer.data:
				section_title = item.pop("section_title")
				if section_title not in support_data:
						support_data[section_title] = []
				support_data[section_title].append(item)

		support_links_data = []
		for section_title, links in support_data.items():
				support_links_data.append(
						{
								"title": section_title,
								"links": links,
						}
				)

		return Response(support_links_data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def post_mood(request):
    serializer = MoodSerializer(data=request.data)

    if serializer.is_valid():
        mood = serializer.save(user=request.user)
        update_streak(mood.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def update_streak(user):
    latest_mood = Mood.objects.filter(user=user).order_by('-mood_date').first()
    if latest_mood:
        # Calculate the difference in days between the current date and the last mood date
        delta = timezone.now().date() - latest_mood.mood_date.date()
        
        if delta.days == 1:
            # Increment streak if the last mood was posted the previous day
            user.profile.streak_count += 1
        elif delta.days > 1:
            # Reset streak if there's a gap of more than one day
            user.profile.streak_count = 1
        user.profile.save()

def get_csrf_token(request):
		csrf_token = get_token(request)
		logger.debug(f"CSRF Token generated: {csrf_token}")
		logger.debug(f"Request META: {request.META}")
		return JsonResponse({'csrf_token': csrf_token})

@api_view(["GET"])
def get_mood_causes(request):
		causes = [cause[0] for cause in MoodCause.CAUSE_CHOICES]
		return JsonResponse(causes, safe=False)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_moods(request, user_id):
		user = request.user
		if str(user.id) == user_id:
				moods = Mood.objects.filter(user=user).order_by("-mood_date")
				serializer = MoodSerializer(moods, many=True)
				return Response(serializer.data)
		else:
				return Response(
						{"error": "You do not have permission to view these moods."}, status=403
				)
		
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_mood(request, mood_id):
		mood = get_object_or_404(Mood, id=mood_id)
		serializer = MoodSerializer(mood, data=request.data, partial=True)
		if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_mood(request, mood_id):
		mood = get_object_or_404(Mood, id=mood_id)
		mood.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_friends_list_view(request):
		friends = Friends.objects.filter(user=request.user, friendship_status="Accepted")
		serializer = FriendSerializer(friends, many=True)
		return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_friend_request(request, username):
    friend_user = get_object_or_404(User, username__iexact=username)
    if request.user == friend_user or Friends.objects.filter(user=request.user, friend=friend_user).exists():
        return Response({"error": "Invalid friend request."}, status=status.HTTP_400_BAD_REQUEST)
    Friends.objects.create(user=request.user, friend=friend_user, friendship_status="Requested")
    return Response({"success": True, "message": "Friend request sent."}, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, username):
    sender_user = get_object_or_404(User, username=username)
    existing_request = Friends.objects.filter(user=sender_user, friend=request.user, friendship_status="Requested").first()
    if existing_request:
        existing_request.friendship_status = "Accepted"
        existing_request.save()
        Friends.objects.create(user=request.user, friend=sender_user, friendship_status="Accepted")
        return Response({"success": True, "message": "Friend request accepted."}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_friend(request, username):
    friend_user = get_object_or_404(User, username=username)
    Friends.objects.filter(user=request.user, friend=friend_user).delete()
    Friends.objects.filter(user=friend_user, friend=request.user).delete()
    return Response({"success": True, "message": "Friend removed."}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reject_friend_request(request, username):
		friend_user = get_object_or_404(User, username=username)
		Friends.objects.filter(user=friend_user, friend=request.user).delete()
		return Response({"success": True, "message": "Friend request rejected."}, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_friend_requests(request):
		friend_requests = Friends.objects.filter(friend=request.user, friendship_status="Requested")
		serializer = FriendRequestSerializer(friend_requests, many=True)
		return Response(serializer.data)

@api_view(['GET'])
def mood_statistics(request):
		mood_counts = Mood.objects.values('mood_type').annotate(count=Count('mood_type'))
		return Response(mood_counts)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def save_broadcast_message(request):
		message = request.data.get('message')
		if message:
				BroadcastMessage.objects.create(message=message)
				return Response({"message": "Broadcast message saved successfully"})
		return Response({"error": "No message provided"}, status=400)

@api_view(['GET'])
def get_latest_broadcast_message(request):
		latest_message = BroadcastMessage.objects.last()
		if latest_message:
				return Response({"message": latest_message.message})
		return Response({"message": ""})

@api_view(['GET'])
def get_users(request):
		search = request.query_params.get('search')
		users = User.objects.all()
		if search:
				users = users.filter(username__icontains=search)

		user_data = []
		for user in users:
				user_moods = Mood.objects.filter(user=user)
				serializer = MoodSerializer(user_moods, many=True)
				user_data.append({
						'username': user.username,
						'first_name': user.first_name,
						'last_name': user.last_name,
						'moods': serializer.data,
						'email': user.email,
				})

		return Response(user_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user_profile(request):
    user = request.user
    profile_picture = request.FILES.get('profilePicture')
    show_mood = request.data.get('showMood') == 'true'

    if profile_picture:
        file_path = default_storage.save(f'profile_pictures/{user.username}/{profile_picture.name}', profile_picture)
        profile_info, created = ProfileInfo.objects.get_or_create(user=user)
        profile_info.picture = file_path
        profile_info.save()
        new_profile_picture_url = f"{settings.MEDIA_URL}{profile_info.picture}"
    else:
        new_profile_picture_url = user.profileinfo.picture.url if hasattr(user, 'profileinfo') and user.profileinfo.picture else None

    user_profile, created = UserProfile.objects.get_or_create(user=user)
    user_profile.show_mood = show_mood
    user_profile.save()

    return Response({
        "message": "Profile updated successfully", 
        "newProfilePictureUrl": new_profile_picture_url
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request, username):
       user = User.objects.get(username=username)
       user_profile = UserProfile.objects.get(user=user)
       serializer = UserProfileSerializer(user_profile)
       return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_show_mood_preference(request):
    user = request.user
    show_mood = request.data.get('showMood')

    user_profile, created = UserProfile.objects.get_or_create(user=user)
    user_profile.show_mood = show_mood
    user_profile.save()

    return Response({"message": "Preference updated successfully"}, status=status.HTTP_200_OK)