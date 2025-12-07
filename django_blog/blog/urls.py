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
    
    # --- Task 2: CRUD URLs ---
    
    # READ: List all posts
    path('posts/', PostListView.as_view(), name='posts'),
    
    # CREATE: New post (Authenticated users only)
    path('posts/new/', PostCreateView.as_view(), name='post-create'),
    
    # READ: Detail view for a single post (Uses the primary key 'pk')
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    
    # UPDATE: Edit an existing post (Author only)
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),
    
    # DELETE: Delete a post (Author only)
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]
