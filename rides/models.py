from django.contrib.gis.db import models as gis_models
from django.db import models

from users.models import User

optional = {
    'null': True,
    'blank': True
}


class Rides(models.Model):
    RIDE_STATUS_DROPOFF = "dropoff"
    RIDE_STATUS_EN_ROUTE = "enroute"
    RIDE_STATUS_PENDING = "pending"
    RIDE_STATUS_PICKUP = "pickup"

    RIDE_STATUSES = (
        (RIDE_STATUS_DROPOFF, "Dropoff"),
        (RIDE_STATUS_EN_ROUTE, "En Route"),
        (RIDE_STATUS_PENDING, "Pending"),
        (RIDE_STATUS_PICKUP, "Pickup"),
    )

    driver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ride_driver"
    )
    rider = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ride_rider"
    )
    dropoff_latitude = models.FloatField(**optional)
    dropoff_longitude = models.FloatField(**optional)
    pickup_latitude = models.FloatField(**optional)
    pickup_longitude = models.FloatField(**optional)
    pickup_time = models.DateTimeField(auto_now_add=True, **optional)
    status = models.CharField(
        max_length=16,
        choices=RIDE_STATUSES,
        default=RIDE_STATUS_PENDING
    )
    pickup_location = gis_models.PointField(**optional)
    dropoff_location = gis_models.PointField(**optional)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ride"
        verbose_name_plural = "Rides"

    def __str__(self):
        return f"Ride {self.id} from {self.pickup_location} to {self.dropoff_location}"


class RideEvents(models.Model):
    ride = models.ForeignKey(
        Rides,
        on_delete=models.CASCADE,
        related_name="ride_event_ride"
    )
    description = models.CharField(max_length=200, **optional)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ride Event"
        verbose_name_plural = "Ride Events"

    def __str__(self):
        return str(self.id)
