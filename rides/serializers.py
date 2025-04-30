from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point

from rest_framework import serializers

from rides.models import Rides, RideEvents
from users.serializers import CustomUserSerializer

User = get_user_model()


class RideEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = RideEvents
        fields = ('id', 'description', 'created_at',)


class RideSerializer(serializers.ModelSerializer):
    pickup_latitude = serializers.FloatField(required=True)
    pickup_longitude = serializers.FloatField(required=True)
    dropoff_latitude = serializers.FloatField(required=True)
    dropoff_longitude = serializers.FloatField(required=True)
    rider = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    driver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    rider_details = CustomUserSerializer(source='rider', read_only=True)
    driver_details = CustomUserSerializer(source='driver', read_only=True)
    travel_distance = serializers.SerializerMethodField()
    todays_ride_events = serializers.SerializerMethodField()
    trip_duration = serializers.SerializerMethodField()

    class Meta:
        model = Rides
        fields = (
            'id',
            'rider',
            'driver',
            'rider_details',
            'driver_details',
            'pickup_latitude',
            'pickup_longitude',
            'dropoff_latitude',
            'dropoff_longitude',
            'pickup_time',
            'status',
            'travel_distance',
            'todays_ride_events',
            'trip_duration',
            'created_at',
            'updated_at',
        )

    def create(self, validated_data):
        ride = super().create(validated_data)
        ride.pickup_location = Point(ride.pickup_longitude, ride.pickup_latitude)
        ride.save()

        return ride

    def update(self, instance, validated_data):
        ride = super().update(instance, validated_data)
        ride.dropoff_location = Point(ride.dropoff_latitude, ride.dropoff_longitude)
        ride.save()

        return ride

    def _build_description(self, ride):
        pickup_coordinates = f"({ride.pickup_latitude}, {ride.pickup_longitude})"
        dropoff_coordinates = f"({ride.dropoff_latitude}, {ride.dropoff_longitude})"
        return f"Status changed to pickup from {pickup_coordinates} to {dropoff_coordinates}"

    def get_todays_ride_events(self, obj):
        recent_24h = self.context.get('recent_ride_events', {}).get(obj.id, [])
        return RideEventSerializer(recent_24h, many=True).data

    def get_travel_distance(self, obj):
        if obj.pickup_latitude and obj.pickup_longitude and obj.dropoff_latitude and obj.dropoff_longitude:
            pickup_point = Point(obj.pickup_longitude, obj.pickup_latitude, srid=4326)
            dropoff_point = Point(obj.dropoff_longitude, obj.dropoff_latitude, srid=4326)
            return f"{round(pickup_point.distance(dropoff_point) * 100000, 2)} meters"
        return None

    def get_trip_duration(self, obj):
        events = self.context.get('recent_ride_events', {}).get(obj.id, [])
        pickup_time = dropoff_time = None

        for event in events:
            if event.description == 'Status changed to pickup':
                pickup_time = event.created_at
            elif event.description == 'Status changed to dropoff':
                dropoff_time = event.created_at

        if pickup_time and dropoff_time:
            duration = dropoff_time - pickup_time
            return duration.total_seconds()
        return None