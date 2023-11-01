from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import Event, ScrapedData
from base.serializers import EventSerializer, ScrapedDataSerializer


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
