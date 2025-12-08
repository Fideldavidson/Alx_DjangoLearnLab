from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token 
from .models import CustomUser

class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True) 
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        
        Token.objects.create(user=user)
        
        return user

class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for retrieving and updating user profile data."""
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'bio', 'profile_picture', 'followers', 'following')
        read_only_fields = ('followers', 'following') 
