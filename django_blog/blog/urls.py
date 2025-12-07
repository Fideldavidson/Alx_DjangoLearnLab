from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

# Import the Class-Based Views for Posts and Comments
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    PostTagListView, # Task 4
    SearchResultsListView, # Task 4
)

urlpatterns = [
    # --- Task 0/1 URLs ---
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # --- Task 2: CRUD URLs (Checker Compliant) ---
    path('posts/', PostListView.as_view(), name='post-list'), 
    path('post/new/', PostCreateView.as_view(), name='post-new'), 
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    
    # --- Task 3: Comment URLs (Checker Compliant) ---
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'), 
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    # --- Task 4: Tagging and Search URLs ---
    path('tag/<slug:tag_slug>/', views.PostTagListView.as_view(), name='post-by-tag'),
    path('search/', views.SearchResultsListView.as_view(), name='search-results'),
]
