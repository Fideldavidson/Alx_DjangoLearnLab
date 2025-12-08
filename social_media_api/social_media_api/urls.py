from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Accounts/Auth URLs
    path('api/', include('accounts.urls')), 
    # Posts/Comments URLs (Task 1 & 3 Likes)
    path('api/', include('posts.urls')), 
    # Notifications URLs (Task 3) - New line
    path('api/', include('notifications.urls')),
]
