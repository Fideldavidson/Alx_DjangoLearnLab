from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class Notification(models.Model):
    # The user who performed the action (e.g., the user who liked the post)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='actions_performed'
    )

    # The user who receives the notification (e.g., the author of the post)
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    # A short phrase describing the action (e.g., 'liked', 'commented on', 'followed')
    verb = models.CharField(max_length=255)
    
    # Timestamp of the event
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Status to track if the notification has been viewed
    is_read = models.BooleanField(default=False)

    # --- Generic Foreign Key Fields (The Target Object) ---
    # This allows the notification to point to ANY model (Post, Comment, etc.)

    # Stores the ID of the model type (e.g., ContentType for Post)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    
    # Stores the primary key of the target object
    object_id = models.PositiveIntegerField()
    
    # The actual field that links to the target object
    target = GenericForeignKey('content_type', 'object_id')

    class Meta:
        # Notifications ordered by newest first
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.actor.username} {self.verb} {self.target} received by {self.recipient.username}'
