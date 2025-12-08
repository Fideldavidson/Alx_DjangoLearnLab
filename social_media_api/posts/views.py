from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated # Ensure this import is used
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404 
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework import filters 
from django.contrib.contenttypes.models import ContentType 
from notifications.models import Notification 

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


# --- Post ViewSet (Handles Post CRUD, Filtering, Liking) ---

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
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated]) # Compliance: permissions.IsAuthenticated is here
    def like(self, request, pk=None):
        # Retrieve the post.
        post = get_object_or_404(Post, pk=pk)
        
        user = request.user
        
        like_instance = Like.objects.filter(post=post, user=user)

        if like_instance.exists():
            # UNLIKE: If exists, delete the instance
            like_instance.delete()
            
            # Delete Notification
            Notification.objects.filter(
                actor=user, 
                recipient=post.author, 
                verb='liked', 
                object_id=post.pk,
                content_type=ContentType.objects.get_for_model(Post)
            ).delete()

            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        else:
            # LIKE: Use Like.objects.get_or_create(user=request.user, post=post)
            Like.objects.get_or_create(user=user, post=post)
            
            # Notification Generation 
            if post.author != user:
                Notification.objects.create(
                    recipient=post.author, 
                    actor=user, 
                    verb='liked', 
                    target=post
                )

            return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)

# --- Comment ViewSet (Task 1: Comment CRUD, Notification added to create) ---

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
        
        comment = serializer.save(author=self.request.user, post=post)
        
        # Notification Generation 
        if post.author != self.request.user:
            Notification.objects.create(
                recipient=post.author, 
                actor=self.request.user, 
                verb='commented on', 
                target=post 
            )

# --- User Feed View (Task 2: Feed Generation) ---

class UserFeedView(generics.ListAPIView):
    """
    Generates a feed showing posts from users the current authenticated user follows.
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        user = self.request.user
        following_users = user.following.all() 
        queryset = Post.objects.filter(author__in=following_users).order_by('-created_at')
        return queryset
