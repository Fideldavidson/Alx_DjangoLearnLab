from django.urls import path
from . import views

urlpatterns = [
    path('register', views.UserRegistrationView.as_view(), name='register'), # /register
    path('login', views.UserLoginView.as_view(), name='login'),               # /login
    path('profile', views.UserProfileView.as_view(), name='profile'),         # /profile
]
