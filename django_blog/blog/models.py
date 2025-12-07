from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    # Field to store the title of the post (max length 200 chars)
    title = models.CharField(max_length=200)
    
    # Field for the main content of the post
    content = models.TextField()
    
    # Field to store the publication date. auto_now_add=True sets the date 
    # automatically when the object is first created.
    published_date = models.DateTimeField(auto_now_add=True)
    
    # Foreign key relationship to Django's built-in User model.
    # on_delete=models.CASCADE means that if the User is deleted, 
    # all their related posts are also deleted.
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post-detail', kwargs={'pk': self.pk})

    def __str__(self):
        """String representation of the Post object for the admin site."""
        return self.title


from django.utils import timezone

class Comment(models.Model):
    """
    Model representing a comment on a blog post.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at'] # Display newest comments last (standard blog practice)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title[:20]}'

    def get_absolute_url(self):
        from django.urls import reverse
        # Redirect back to the detail page of the post the comment belongs to
        return reverse('post-detail', kwargs={'pk': self.post.pk})
