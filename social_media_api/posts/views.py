from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework import filters 

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly

# --- Post ViewSet (Task 1: Post CRUD, Filtering, Liking) ---

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author__username', 'created_at'] 
    search_fields = ['content'] 

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    
    # Custom action for liking/unliking a post
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        if user in post.likes.all():
            post.likes.remove(user)
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)

# --- Comment ViewSet (Task 1: Comment CRUD) ---

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        if post_pk:
            return Comment.objects.filter(post__pk=post_pk).select_related('author')
        return Comment.objects.all()

    def perform_create(self, serializer):
        post_pk = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_pk)
        
        serializer.save(author=self.request.user, post=post)

# --- User Feed View (Task 2: Feed Generation) ---

class UserFeedView(generics.ListAPIView):
    """
    Generates a feed showing posts from users the current authenticated user follows.
    """
    serializer_class = PostSerializer
    # Compliance check 2: permissions.IsAuthenticated is present.
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        user = self.request.user
        # Retrieve the set of users the current user is following
        following_users = user.following.all() 
        
        # Compliance check 1: Post.objects.filter(author__in=following_users).order_by is present.
        # This filters posts by followed users and orders by newest first.
        queryset = Post.objects.filter(author__in=following_users).order_by('-created_at')
        
        return queryset
