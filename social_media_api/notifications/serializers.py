from rest_framework import serializers
from .models import Notification
from accounts.serializers import CustomUserSerializer # Reuse CustomUserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    # Display the actor's details
    actor = CustomUserSerializer(read_only=True)
    
    # Read-only field to clearly display the target object's type and ID
    target_type = serializers.SerializerMethodField()
    target_id = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ('id', 'actor', 'verb', 'timestamp', 'is_read', 'target_type', 'target_id')
        read_only_fields = ('actor', 'recipient', 'verb', 'timestamp', 'is_read')

    def get_target_type(self, obj):
        # Returns the name of the model (e.g., 'post', 'user')
        return obj.content_type.model
        
    def get_target_id(self, obj):
        # Returns the primary key of the target object
        return obj.object_id
