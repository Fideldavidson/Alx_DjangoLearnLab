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

    # Blog post CRUD (renamed to match expected format)
    path("post/", PostListView.as_view(), name="posts"),
    path("post/new/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
]
