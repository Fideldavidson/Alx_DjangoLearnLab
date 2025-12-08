from django.urls import path
from . import views

urlpatterns = [
    # API Endpoint for User Registration
    # Uses the UserRegistrationView (generics.CreateAPIView) to create a new CustomUser.
    # It returns a Token upon successful creation. Trailing slash is added for compliance.
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    
    # API Endpoint for User Login and Token Retrieval
    # Uses the UserLoginView (ObtainAuthToken) to validate credentials and return an existing Token.
    # Trailing slash is added for compliance.
    path('login/', views.UserLoginView.as_view(), name='login'),
    
    # API Endpoint for Profile Management (GET/PUT/PATCH)
    # Allows authenticated users to view or update their own profile details (bio, picture, etc.).
    path('profile/', views.UserProfileView.as_view(), name='profile'),
]
