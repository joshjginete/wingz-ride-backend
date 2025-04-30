import logging
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter 
from django_filters.rest_framework import DjangoFilterBackend

from rides.models import Rides
from rides.filters import RideFilter
from rides.serializers import RideSerializer

logger = logging.getLogger(__name__)


class RideViewSet(viewsets.ModelViewSet):
    serializer_class = RideSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = RideFilter
    ordering_fields = ['pickup_time', 'pickup_distance']

    def get_queryset(self):
        queryset = Rides.objects.select_related('rider', 'driver').prefetch_related('ride_event_ride')

        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')

        if latitude and longitude:
            try:
                user_location = Point(float(longitude), float(latitude), srid=4326)
                queryset = queryset.annotate(
                    pickup_distance=Distance('pickup_location', user_location)
                )
            except (ValueError, TypeError) as e:
                logger.warning(f"Invalid latitude/longitude values for distance sorting: latitude={latitude}, longitude={longitude}, error={e}")

        return queryset