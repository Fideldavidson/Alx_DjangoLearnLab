from django.db import models
from django.conf import settings # Import settings to link to the CustomUser model

class Post(models.Model):
    # Foreign Key linking Post to the User who authored it.
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # If the User is deleted, their Posts are also deleted.
        related_name='posts' # Access Posts via user.posts.all()
    )
    
    # Text content of the post.
    content = models.TextField(
        max_length=5000,
        blank=False,
        null=False
    )
    
    # Timestamp for when the post was first created.
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    # Timestamp for the last time the post was updated.
    updated_at = models.DateTimeField(
        auto_now=True
    )
    
    # Many-to-Many field for tracking likes from users.
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='liked_posts',
        blank=True
    )

    class Meta:
        # Default ordering for queries: newest posts first.
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author.username}'s Post ({self.pk})"

# --- Comment Model ---
class Comment(models.Model):
    # Foreign Key linking Comment to its parent Post.
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments' # Access Comments via post.comments.all()
    )
    
    # Foreign Key linking Comment to the User who authored it.
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments' # Access Comments via user.comments.all()
    )
    
    # Text content of the comment.
    content = models.TextField(
        max_length=500,
        blank=False,
        null=False
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        # Default ordering for comments: oldest first (standard comment thread ordering).
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on Post {self.post.pk}"
