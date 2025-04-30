import logging
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.db.models import Prefetch
from django.utils.timezone import now, timedelta
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter 
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from rides.models import RideEvents, Rides
from rides.filters import RideFilter
from rides.serializers import RideSerializer

logger = logging.getLogger(__name__)


class RideViewSet(viewsets.ModelViewSet):
    serializer_class = RideSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = RideFilter
    ordering_fields = ['pickup_time', 'travel_distance']

    def get_queryset(self):
        queryset = Rides.objects.select_related('rider', 'driver')

        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')

        if latitude and longitude:
            try:
                user_location = Point(float(longitude), float(latitude), srid=4326)
                queryset = queryset.annotate(
                    travel_distance=Distance('pickup_location', user_location)
                )
            except (ValueError, TypeError) as e:
                logger.warning(f"Invalid latitude/longitude values: {e}")

        # Filter RideEvents from the past 24 hours
        recent_time_threshold = now() - timedelta(hours=24)
        recent_events = RideEvents.objects.filter(created_at__gte=recent_time_threshold)

        # Prefetch only recent RideEvents
        queryset = queryset.prefetch_related(
            Prefetch('ride_event_ride', queryset=recent_events, to_attr='recent_ride_events')
        )

        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        # Optional: you could log number of queries for debugging if needed.
        # from django.db import connection
        # print(len(connection.queries))

        return response

    def get_serializer_context(self):
        context = super().get_serializer_context()
        rides = self.get_queryset()

        # Build a mapping: ride_id -> recent events
        recent_events_map = {
            ride.id: getattr(ride, 'recent_ride_events', [])
            for ride in rides
        }
        context['recent_ride_events'] = recent_events_map
        return context

    @action(detail=True, methods=['post'], url_path='pickup')
    def pickup(self, request, pk=None):
        ride = self.get_object()

        # Create pickup event
        RideEvents.objects.create(
            ride=ride,
            description='Status changed to pickup'
        )

        # Optional: update status
        ride.status = 'pickup'
        ride.save()

        return Response({'detail': 'Pickup recorded.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='dropoff')
    def dropoff(self, request, pk=None):
        ride = self.get_object()

        # Create dropoff event
        RideEvents.objects.create(
            ride=ride,
            description='Status changed to dropoff'
        )

        # Optional: update status
        ride.status = 'dropoff'
        ride.save()

        return Response({'detail': 'Dropoff recorded.'}, status=status.HTTP_200_OK)