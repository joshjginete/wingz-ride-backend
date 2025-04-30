from rest_framework import viewsets

from django_filters.rest_framework import DjangoFilterBackend

from rides.models import Rides
from rides.filters import RideFilter
from rides.serializers import RideSerializer


class RideViewSet(viewsets.ModelViewSet):
    queryset = Rides.objects.select_related('rider', 'driver').prefetch_related('ride_event_ride').all()
    serializer_class = RideSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'driver', 'rider']
