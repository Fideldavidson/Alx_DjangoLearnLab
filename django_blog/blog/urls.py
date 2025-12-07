from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# Import the Class-Based Views
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

urlpatterns = [
    # --- Task 0/1 URLs ---
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # --- Task 2: CRUD URLs (Checker Compliant) ---
    
    # READ: List all posts
    path('posts/', PostListView.as_view(), name='post-list'), # Changed name from 'posts' to 'post-list' 
    
    # CREATE: New post
    path('post/new/', PostCreateView.as_view(), name='post-new'), # Checker required path 'post/new/' and name 'post-new'
    
    # READ: Detail view for a single post
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    
    # UPDATE: Edit an existing post
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'), # Checker required path 'post/<int:pk>/update/'
    
    # DELETE: Delete a post
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'), # Checker required path 'post/<int:pk>/delete/'
]
