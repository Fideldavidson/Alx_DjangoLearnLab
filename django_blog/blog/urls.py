from django.urls import path
from . import views

urlpatterns = [
    # Map the root of the blog app to the post_list view
    path('', views.post_list, name='post_list'),
]
