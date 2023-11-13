from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from base.models import Event, ScrapedData, Mood, SupportLink, MoodCause
from base.serializers import (
    EventSerializer,
    ScrapedDataSerializer,
    SupportLinkSerializer,
    CustomSupportLinkSerializer,
    MoodSerializer,
    MoodCauseSerializer,
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
