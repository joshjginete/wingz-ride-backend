from rest_framework.routers import DefaultRouter
from django.urls import path, include

from rides.views import RideViewSet

router = DefaultRouter()
router.register(r'rides', RideViewSet, basename='ride')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
