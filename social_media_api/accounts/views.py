from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from .serializers import CustomUserRegistrationSerializer, CustomUserSerializer
from .models import CustomUser

# --- User Registration and Login ---

class UserRegistrationView(generics.CreateAPIView):
    """Handles user registration and returns a token."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # Fetch the newly created user (by username is easiest here)
        user = CustomUser.objects.get(username=request.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        
        # Return the required token upon successful registration
        return Response({
            'user_id': user.pk,
            'username': user.username,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


class UserLoginView(ObtainAuthToken):
    """Handles user login (username/password) and returns a token."""
    # ObtainAuthToken automatically handles the validation and token retrieval.
    # We override post() to customize the response format.
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        
        return Response({
            'user_id': user.pk,
            'username': user.username,
            'token': token.key
        })

# --- Profile Management ---

class UserProfileView(generics.RetrieveUpdateAPIView):
    """Allows authenticated users to view/update their own profile."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Ensure only the logged-in user can access their own profile
        return self.request.user
