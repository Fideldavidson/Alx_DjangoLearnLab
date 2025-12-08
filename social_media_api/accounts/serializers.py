from rest_framework import serializers
from .models import CustomUser

class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    class Meta:
        model = CustomUser
        # Fields for registration
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

class CustomUserSerializer(serializers.ModelSerializer):
    """Serializer for retrieving and updating user profile data."""
    # Note: 'followers' and 'following' fields are included here due to the model definition
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'bio', 'profile_picture', 'followers', 'following')
        read_only_fields = ('followers', 'following') 
