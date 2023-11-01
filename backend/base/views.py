from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from base.models import Event, ScrapedData
from base.serializers import EventSerializer, ScrapedDataSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    # Check if all required fields are present
    if not all([username, password, email, first_name, last_name]):
        return Response({'error': 'All fields are required!'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists!'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the user with the required fields
    user = User.objects.create_user(
        username=username, 
        password=password, 
        email=email, 
        first_name=first_name, 
        last_name=last_name
    )
    return Response({'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({'error': 'All fields are required!'}, status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)

    if user:
        return Response({'message': 'Login successful!'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials!'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view()
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({'message': 'connected !'}, 200)

@api_view(['GET'])
def get_events(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_scraped_data(request):
    scraped_data = ScrapedData.objects.all()
    serializer = ScrapedDataSerializer(scraped_data, many=True)
    return Response(serializer.data)
