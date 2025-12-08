from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework import filters 
from django.contrib.contenttypes.models import ContentType # Required for Notifications

from .models import Post, Comment, Like # New: Import Like model
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from notifications.models import Notification # New: Import Notification model


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
    
    # Custom action for liking/unliking a post (Task 3 enhancement)
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        # Check if the user has already liked the post
        like_instance = Like.objects.filter(post=post, user=user)

        if like_instance.exists():
            # If exists, unlike (remove the instance)
            like_instance.delete()
            
            # Optional: Delete Notification on unlike (simplification)
            Notification.objects.filter(
                actor=user, 
                recipient=post.author, 
                verb='liked', 
                object_id=post.pk,
                content_type=ContentType.objects.get_for_model(Post)
            ).delete()

            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        else:
            # If not exists, like (create the instance)
            Like.objects.create(post=post, user=user)
            
            # Notification Generation (Step 3)
            # Notify the post author only if they didn't like their own post
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
        
        # Notification Generation (Step 3): Notify post author of a new comment
        if post.author != self.request.user:
            Notification.objects.create(
                recipient=post.author, 
                actor=self.request.user, 
                verb='commented on', 
                target=post # Target is the Post object
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
