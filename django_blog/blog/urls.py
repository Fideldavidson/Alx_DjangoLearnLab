from django.urls import path
from django.contrib.auth import views as auth_views # Import built-in auth views
from . import views

urlpatterns = [
    # --- Task 0 URLs ---
    path('', views.home, name='home'),
    path('posts/', views.post_list, name='posts'),
    
    # --- Task 1 Authentication URLs ---
    
    # 1. Registration
    path('register/', views.register, name='register'),
    
    # 2. Login (Uses built-in view)
    path('login/', 
         auth_views.LoginView.as_view(template_name='blog/login.html'), 
         name='login'),
         
    # 3. Logout (Uses built-in view)
    path('logout/', 
         auth_views.LogoutView.as_view(template_name='blog/logout.html'), 
         name='logout'),
         
    # 4. Profile Management
    path('profile/', views.profile, name='profile'),
]
