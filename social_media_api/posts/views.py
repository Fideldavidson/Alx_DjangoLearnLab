from rest_framework import viewsets, mixins, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend # For filtering/searching
from rest_framework import filters # For ordering/searching

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly

# --- Post ViewSet (Handles Post CRUD, Pagination, Filtering) ---

class PostViewSet(viewsets.ModelViewSet):
    # Basic queryset and serializer setup
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    # Permissions: Users can view all posts, but only authenticated users can create.
    # Users can only edit/delete their own posts.
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    # Step 5: Implement Filtering and Pagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author__username', 'created_at'] # Allows filtering by author name or date
    # Allows searching content by title or content fields
    search_fields = ['content'] 

    def perform_create(self, serializer):
        # Automatically set the author to the requesting user upon creation
        serializer.save(author=self.request.user)
    
    # Custom action for liking/unliking a post
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        # Retrieve the specific post object
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        # Check if the user has already liked the post
        if user in post.likes.all():
            # If liked, unlike it
            post.likes.remove(user)
            return Response({'status': 'unliked'}, status=status.HTTP_200_OK)
        else:
            # If not liked, like it
            post.likes.add(user)
            return Response({'status': 'liked'}, status=status.HTTP_201_CREATED)

# --- Comment ViewSet (Handles Comment CRUD) ---

class CommentViewSet(viewsets.ModelViewSet):
    # We will filter the queryset in get_queryset()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    
    def get_queryset(self):
        # We assume comments are always listed relative to a specific post 
        # (e.g., /api/posts/1/comments/)
        post_pk = self.kwargs.get('post_pk')
        if post_pk:
            return Comment.objects.filter(post__pk=post_pk).select_related('author')
        return Comment.objects.all()

    def perform_create(self, serializer):
        # When creating a comment, automatically link it to the post and the author
        post_pk = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_pk)
        
        # Save the comment, setting the required fields
        serializer.save(author=self.request.user, post=post)
from rest_framework import generics # Import generics for the new FeedView

# --- New Feed View (Task 2) ---

class UserFeedView(generics.ListAPIView):
    """
    Generates a feed showing posts from users the current authenticated user follows.
    Posts are ordered by creation date (newest first).
    """
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated] # Only authenticated users can access their feed

    def get_queryset(self):
        # 1. Get the current authenticated user
        user = self.request.user
        
        # 2. Get the IDs of users the current user is following
        # We access the list of followed users via the 'following' related manager (defined on CustomUser model)
        followed_users = user.following.all()
        
        # 3. Retrieve posts only from those followed users
        # Filter posts where the author is in the list of followed users.
        queryset = Post.objects.filter(author__in=followed_users).order_by('-created_at')
        
        # The queryset will automatically be paginated by the settings
        return queryset
