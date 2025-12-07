from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy

# Import the base CBVs
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .forms import CustomUserCreationForm, PostForm
from .models import Post


# --- Task 0/1 Views (Retained) ---
# Home view remains functional for the root path
def home(request):
    return render(request, 'blog/home.html', {})

# Registration view remains functional
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}. You can now log in!')
            return redirect('login') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

# Profile view remains functional
@login_required
def profile(request):
    if request.method == 'POST':
        user = request.user
        new_email = request.POST.get('email')
        
        if new_email and new_email != user.email:
            if User.objects.filter(email=new_email).exclude(id=user.id).exists():
                messages.error(request, "This email address is already taken by another user.")
            else:
                user.email = new_email
                user.save()
                messages.success(request, "Your profile has been updated successfully.")
        return redirect('profile')

    return render(request, 'blog/profile.html', {'user': request.user})


# --- Task 2: CRUD Class-Based Views ---

# 1. READ: Display list of all posts (Accessible to all users)
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # <app>/<model>_list.html
    context_object_name = 'posts'  # Name of the list object in the template
    ordering = ['-published_date'] # Order by newest first

# 2. READ: Display individual post details (Accessible to all users)
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html' # <app>/<model>_detail.html
    context_object_name = 'post'

# 3. CREATE: Allow authenticated users to create a new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('posts') # Redirect to the post list after creation

    # Set the author to the currently logged-in user before saving
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Your post has been created successfully!")
        return super().form_valid(form)

# 4. UPDATE: Allow post authors to edit their posts
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    # success_url is automatically taken from the model's get_absolute_url if not set

    # Test function to ensure only the author can update the post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def form_valid(self, form):
        messages.success(self.request, "Your post has been updated successfully!")
        return super().form_valid(form)

# 5. DELETE: Allow post authors to delete their posts
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('posts') # Redirect to the post list after deletion
    context_object_name = 'post'

    # Test function to ensure only the author can delete the post
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def form_valid(self, form):
        messages.success(self.request, "Your post has been deleted successfully!")
        return super().form_valid(form)

# The dummy post_list view from Task 0 is removed as it's replaced by PostListView.
