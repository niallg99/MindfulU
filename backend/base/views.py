from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from base.models import Event, ScrapedData, Mood, SupportLink, MoodCause, Friends
from base.serializers import (
    EventSerializer,
    ScrapedDataSerializer,
    SupportLinkSerializer,
    CustomSupportLinkSerializer,
    MoodSerializer,
    MoodCauseSerializer,
    FriendSerializer,
)


@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    first_name = request.data.get("first_name")
    last_name = request.data.get("last_name")

    # Check if all required fields are present
    if not all([username, password, email, first_name, last_name]):
        return Response(
            {"error": "All fields are required!"}, status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists!"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Create the user with the required fields
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
        # Generate the access token and include it in the response
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

    # Explicitly create a Response object and set the data attribute
    response = Response(serializer.data)

    return response


@api_view(["GET"])
def get_support_links_view(request):
    # Fetch all SupportLink objects and serialize them
    support_links = SupportLink.objects.all()
    serializer = CustomSupportLinkSerializer(support_links, many=True)

    # Group the serialized data by section title
    support_data = {}
    for item in serializer.data:
        section_title = item.pop("section_title")
        if section_title not in support_data:
            support_data[section_title] = []
        support_data[section_title].append(item)

    # Transform the grouped data into the desired format
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
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_friends_list_view(request):
    friends = Friends.objects.filter(user=request.user)
    serializer = FriendSerializer(friends, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_friends(request, user_id):
    if str(request.user.id) == user_id:
        friends = Friends.objects.filter(user=request.user)
        serializer = FriendSerializer(friends, many=True)
        return Response(serializer.data)
    else:
        return Response({"error": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
    
from django.shortcuts import get_object_or_404

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_friend_request(request, username):
    # Get the user object for the given username
    friend_user = get_object_or_404(User, username=username)
    # Check if the friend request already exists or if it's a request to oneself
    if request.user == friend_user or Friends.objects.filter(user=request.user, friend=friend_user).exists():
        return Response({"error": "Invalid friend request."}, status=status.HTTP_400_BAD_REQUEST)
    # Create a new friend request
    Friends.objects.create(user=request.user, friend=friend_user, friendship_status="Requested")
    return Response({"message": "Friend request sent."}, status=status.HTTP_200_OK)


# Accept Friend Request
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, friend_id):
    friend_request = get_object_or_404(Friends, user_id=friend_id, friend=request.user)
    friend_request.friendship_status = "Accepted"
    friend_request.save()
    return Response({"message": "Friend request accepted."}, status=status.HTTP_200_OK)

# Reject Friend Request
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reject_friend_request(request, friend_id):
    Friends.objects.filter(user_id=friend_id, friend=request.user).delete()
    return Response({"message": "Friend request rejected."}, status=status.HTTP_200_OK)

# Remove Friend
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_friend(request, friend_id):
    Friends.objects.filter(user=request.user, friend_id=friend_id).delete()
    return Response({"message": "Friend removed."}, status=status.HTTP_200_OK)


