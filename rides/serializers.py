from django.contrib.auth import get_user_model

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
    ride_event_ride = RideEventSerializer(many=True, read_only=True)

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
            'created_at',
            'updated_at',
            'ride_event_ride',
        )

    def create(self, validated_data):
        ride = super().create(validated_data)
        RideEvents.objects.create(
            ride=ride,
            description=self._build_description(ride, action="created")
        )
        return ride

    def update(self, instance, validated_data):
        ride = super().update(instance, validated_data)
        RideEvents.objects.create(
            ride=ride,
            description=self._build_description(ride, action="updated")
        )
        return ride

    def _build_description(self, ride, action):
        pickup = f"({ride.pickup_latitude}, {ride.pickup_longitude})"
        dropoff = f"({ride.dropoff_latitude}, {ride.dropoff_longitude})"
        return f"Ride {action} from {pickup} to {dropoff}"
