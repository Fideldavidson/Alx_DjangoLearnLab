from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import CustomUserRegistrationSerializer, CustomUserSerializer
from .models import CustomUser
from notifications.models import Notification # New: Import Notification model

# --- User Registration and Login Views (Task 0) ---

class UserRegistrationView(generics.CreateAPIView):
    """Handles user registration and returns a token."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = CustomUser.objects.get(username=request.data['username'])
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user_id': user.pk,
            'username': user.username,
            'token': token.key
        }, status=status.HTTP_201_CREATED)


class UserLoginView(ObtainAuthToken):
    """Handles user login (username/password) and returns a token."""
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        return Response({
            'user_id': user.pk,
            'username': user.username,
            'token': token.key
        })

class UserProfileView(generics.RetrieveUpdateAPIView):
    """Allows authenticated users to view/update their own profile."""
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# --- Follow Management Views (Task 2 & 3: Notification Added) ---

class FollowUserView(generics.GenericAPIView):
    """Allows an authenticated user to follow another user."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id, format=None):
        user_to_follow = get_object_or_404(CustomUser, pk=user_id)
        current_user = request.user 
        
        if user_to_follow == current_user:
            return Response({"detail": "Cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Add the relationship
        current_user.following.add(user_to_follow)
        
        # Notification Generation (Step 3)
        Notification.objects.create(
            recipient=user_to_follow, 
            actor=current_user, 
            verb='started following', 
            target=user_to_follow # Target is the User who was followed
        )
        
        return Response(
            {"detail": f"Now following {user_to_follow.username}"}, 
            status=status.HTTP_201_CREATED
        )


class UnfollowUserView(generics.GenericAPIView):
    """Allows an authenticated user to unfollow another user."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id, format=None):
        user_to_unfollow = get_object_or_404(CustomUser, pk=user_id)
        current_user = request.user
        
        # Remove the relationship
        current_user.following.remove(user_to_unfollow)
        
        # Optional: Delete Notification on unfollow
        Notification.objects.filter(
            actor=current_user, 
            recipient=user_to_unfollow, 
            verb='started following'
        ).delete()
        
        return Response(
            {"detail": f"Unfollowed {user_to_unfollow.username}"}, 
            status=status.HTTP_200_OK
        )
