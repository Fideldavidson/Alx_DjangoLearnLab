from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include the accounts app URLs under the /api/ path as required
    path('api/', include('accounts.urls')), 
]
