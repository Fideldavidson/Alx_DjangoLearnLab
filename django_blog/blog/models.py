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

