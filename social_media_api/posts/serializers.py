from rest_framework import serializers
from .models import Post, Comment
from accounts.serializers import CustomUserSerializer 

# --- Comment Serializer ---
class CommentSerializer(serializers.ModelSerializer):
    # Nested serializer to display the author's details instead of just ID
    author = CustomUserSerializer(read_only=True) 
    
    # This field is required for the PostDetailView to receive the post ID
    post_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'post_id', 'author', 'content', 'created_at', 'updated_at')
        # post is read-only because it's set on the server side or linked via post_id
        read_only_fields = ('post', 'author', 'created_at', 'updated_at')

# --- Post Serializer ---
class PostSerializer(serializers.ModelSerializer):
    # Nested serializer for the author
    author = CustomUserSerializer(read_only=True) 
    
    # Nested serializer for comments (read-only list on the detail view)
    comments = CommentSerializer(many=True, read_only=True) 
    
    # Read-only field to display the count of likes
    likes_count = serializers.SerializerMethodField()
    
    # Boolean field indicating if the requesting user has liked the post (useful for UI)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'author', 'content', 'created_at', 'updated_at',
            'likes', 'likes_count', 'is_liked', 'comments'
        )
        # Author, timestamps, and likes list are set/managed by the server
        read_only_fields = ('author', 'created_at', 'updated_at', 'likes') 

    def get_likes_count(self, obj):
        # Compute and return the number of likes
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        # Check if the requesting user is in the 'likes' queryset
        user = self.context['request'].user
        if user.is_authenticated:
            # Check if the user is in the list of users who liked this post
            return obj.likes.filter(pk=user.pk).exists()
        return False
