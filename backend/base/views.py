from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from base.models import Event, ScrapedData, Mood, SupportLink, MoodCause, Friends
from base.serializers import (
    EventSerializer,
    ScrapedDataSerializer,
    SupportLinkSerializer,
    CustomSupportLinkSerializer,
    MoodSerializer,
    FriendSerializer,
    FriendRequestSerializer,
)

@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")

    if not all([username, password, email, first_name, last_name]):
        return Response(
            {"error": "All fields are required!"}, status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists!"}, status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    return Response(
        {"message": "User registered successfully!"}, status=status.HTTP_201_CREATED
    )

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
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrf_token": csrf_token})

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
    friend_user = get_object_or_404(User, username=username)
    if request.user == friend_user or Friends.objects.filter(user=request.user, friend=friend_user).exists():
        return Response({"error": "Invalid friend request."}, status=status.HTTP_400_BAD_REQUEST)
    Friends.objects.create(user=request.user, friend=friend_user, friendship_status="Requested")
    return Response({"message": "Friend request sent."}, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, username):
    friend_user = get_object_or_404(User, username=username)
    friend_request = get_object_or_404(Friends, user=friend_user, friend=request.user)
    friend_request.friendship_status = "Accepted"
    friend_request.save()
    return Response({"message": "Friend request accepted."}, status=status.HTTP_200_OK)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reject_friend_request(request, username):
    friend_user = get_object_or_404(User, username=username)
    Friends.objects.filter(user=friend_user, friend=request.user).delete()
    return Response({"message": "Friend request rejected."}, status=status.HTTP_200_OK)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_friend(request, username):
    friend_user = get_object_or_404(User, username=username)
    Friends.objects.filter(user=request.user, friend=friend_user).delete()
    return Response({"message": "Friend removed."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_friend_requests(request):
    friend_requests = Friends.objects.filter(friend=request.user, friendship_status="Requested")
    serializer = FriendRequestSerializer(friend_requests, many=True)
    return Response(serializer.data)


