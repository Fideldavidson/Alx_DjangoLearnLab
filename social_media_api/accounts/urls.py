from django.urls import path
from . import views

urlpatterns = [
    # API Endpoint for User Registration (Task 0)
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    
    # API Endpoint for User Login and Token Retrieval (Task 0)
    path('login/', views.UserLoginView.as_view(), name='login'),
    
    # API Endpoint for Profile Management (Task 0)
    path('profile/', views.UserProfileView.as_view(), name='profile'),
    
    # New Follow/Unfollow Endpoints (Task 2)
    path('follow/<int:user_id>/', views.FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', views.UnfollowUserView.as_view(), name='unfollow-user'),
]
