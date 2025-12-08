from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    """
    Allows an authenticated user to view their notifications.
    Filters notifications to only include those belonging to the requesting user.
    """
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Fetch notifications where the recipient is the current authenticated user,
        # ordering by newest first.
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')

class NotificationMarkAsReadView(generics.UpdateAPIView):
    """
    Allows an authenticated user to mark a specific notification as read.
    """
    queryset = Notification.objects.all()
    permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        notification = self.get_object()
        
        # Security check: Ensure the user owns the notification
        if notification.recipient != request.user:
            return Response(
                {"detail": "You do not have permission to modify this notification."}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Mark as read and save
        notification.is_read = True
        notification.save()
        
        return Response({'status': 'marked as read'}, status=status.HTTP_200_OK)
