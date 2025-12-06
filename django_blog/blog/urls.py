from django.urls import path
from .views import (
    BlogLoginView, BlogLogoutView, register, profile, home,
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView
)

urlpatterns = [
    path("", home, name="home"),
    path("login/", BlogLoginView.as_view(), name="login"),
    path("logout/", BlogLogoutView.as_view(), name="logout"),
    path("register/", register, name="register"),
    path("profile/", profile, name="profile"),

    path("posts/", PostListView.as_view(), name="posts"),
    path("posts/new/", PostCreateView.as_view(), name="post-create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:pk>/edit/", PostUpdateView.as_view(), name="post-update"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
]
