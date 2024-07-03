from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, request, viewsets, permissions
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.Profile.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class UserUpdateSerializerUsingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']

    def update(self, instance, validated_data):
        # Only allow superusers to modify all fields
        if self.context['request'].user.is_superuser:
            instance.email = validated_data.get('email', instance.email)
            instance.password = validated_data.get('password', instance.password)
        # Regular users can only modify their email and password
        else:
            instance.email = validated_data.get('email', instance.email)
            instance.set_password(validated_data.get('password'))
        instance.save()
        return instance


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


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return CustomUser.objects.all()
        return CustomUser.objects.filter(id=self.request.user.id)

    def perform_update(self, serializer):
        if not self.request.user.is_superuser and serializer.instance.id != self.request.user.id:
            raise permissions.PermissionDenied("You do not have permission to update this user.")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_superuser and instance.id != self.request.user.id:
            raise permissions.PermissionDenied("You do not have permission to delete this user.")
        instance.delete()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user=user)
        token['username'] = user.username
        token['email'] = user.email
        print(f'username: {user.username}, email: {user.email}')
        return token


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(validated_data['email'], password=validated_data['password'])
        return user
