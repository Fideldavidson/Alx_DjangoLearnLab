from django.urls import path
from . import views

urlpatterns = [
    # Endpoint to fetch the list of notifications for the current user
    path('notifications/', views.NotificationListView.as_view(), name='notification-list'),
    
    # Endpoint to mark a specific notification as read
    path('notifications/<int:pk>/read/', views.NotificationMarkAsReadView.as_view(), name='notification-read'),
]
