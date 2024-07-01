from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, request
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.Profile.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user=user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # Debugging output
        print(f'username: {user.username}, email: {user.email}')
        return token


from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, request
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.Profile.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user=user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        # Debugging output
        print(f'username: {user.username}, email: {user.email}')
        return token


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(validated_data['email'], password=validated_data['password'])
        return user

