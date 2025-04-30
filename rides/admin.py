from django.contrib import admin

from rides.models import RideEvents, Rides


class RideEventsAdmin(admin.ModelAdmin):
    search_fields = ["id"]
    list_display = [
        "id",
        "ride",
        "description",
        "created_at",
        "updated_at",
    ]


class RidesAdmin(admin.ModelAdmin):
    search_fields = ["id", "driver__username", "rider__username"]
    list_display = [
        "id",
        "driver",
        "rider",
        "pickup_location",
        "dropoff_location",
        "status",
        "created_at",
        "updated_at",
    ]


admin.site.register(RideEvents, RideEventsAdmin)
admin.site.register(Rides, RidesAdmin)
