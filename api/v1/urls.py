from rest_framework.routers import DefaultRouter
from django.urls import path, include

# from rides.views import RideViewSet
from users.views import UserViewSet

router = DefaultRouter()
# router.register(r'rides', RideViewSet, basename='ride')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
]
