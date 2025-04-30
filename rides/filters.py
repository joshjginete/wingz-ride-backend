import django_filters

from rides.models import Rides


class RideFilter(django_filters.FilterSet):
    rider_email = django_filters.CharFilter(field_name='rider__email', lookup_expr='icontains')
    driver_email = django_filters.CharFilter(field_name='driver__email', lookup_expr='icontains')

    class Meta:
        model = Rides
        fields = ['status', 'rider_email', 'driver_email']