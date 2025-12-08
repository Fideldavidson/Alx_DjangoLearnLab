from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Accounts/Auth URLs
    path('api/', include('accounts.urls')), 
    # Posts/Comments URLs (Task 1) - This line includes the required "posts.urls"
    path('api/', include('posts.urls')), 
]
