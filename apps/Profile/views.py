from django.shortcuts import render
from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.Profile.models import CustomUser
from apps.Profile.serializer import RegisterSerializer, CustomTokenObtainPairSerializer, CustomUserSerializer


# Create your views here.
def profile(request):
    return HttpResponse("Profile Working!")


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for obtaining JWT token pair.
    """
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        operation_description="Obtain JWT token pair with custom claims",
        responses={
            200: openapi.Response(description='JWT token pair obtained successfully', schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(type=openapi.TYPE_STRING),
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING),
                }
            )),
            400: "Bad Request"
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete user details.
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=user.id)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CustomUserSerializer(instance, data=request.data, partial=True, exclude_fields=['email', 'password'])
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CustomUserSerializer(instance, data=request.data, partial=True, exclude_fields=['email', 'password'])
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []

    @swagger_auto_schema(operation_description="Register a new user", request_body=CustomUserSerializer)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate tokens securely
            password = request.data.get('password')
            token_serializer = CustomTokenObtainPairSerializer(data={
                'email': user.email,
                'password': password
            })
            token_serializer.is_valid(raise_exception=True)
            tokens = token_serializer.validated_data
            return Response({
                'success': True,
                'message': 'User registered successfully',
                'user': {
                    'id': user.id,
                    'email': user.email
                },
                'tokens': tokens
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    def post(self, request):
        try:
            access_token = request.headers.get('Authorization')
            print(access_token)
            if not access_token:
                return Response({'error': 'access token is required.'}, status=status.HTTP_400_BAD_REQUEST)

            token = AccessToken(access_token)
            token.blacklist()

            return Response({'detail': 'Logout successful.'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': 'Invalid token provided.'}, status=status.HTTP_400_BAD_REQUEST)
