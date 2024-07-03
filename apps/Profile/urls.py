from django.db import router
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.Profile.serializer import UserViewSet
from apps.Profile.views import profile, RegisterApi, CustomTokenObtainPairView, LogoutAPIView, \
    UserDetailView


router = DefaultRouter()
router.register(r'users', UserViewSet)
urlpatterns = [
    path('', profile, name='profile'),
    path('register/', RegisterApi.as_view(), name='register'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('', include(router.urls)),
    path('custom-token-obtain-pair/', CustomTokenObtainPairView.as_view(), name='custom-token-obtain-pair')
]

