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

from .forms import CustomUserCreationForm, PostForm, CommentForm # <-- Ensure CommentForm is imported
from .models import Post, Comment # <-- Ensure Comment model is imported


# --- Task 0/1 Views (Authentication) ---
def home(request):
    return render(request, 'blog/home.html', {})

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


# --- Task 2: CRUD Class-Based Views (Post Management) ---

# 1. READ: Display list of all posts (Public)
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date'] 

# 2. READ: Display individual post details (Public)
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    # --- UPDATED CONTEXT FOR TASK 3 ---
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass an empty CommentForm instance to the template
        context['comment_form'] = CommentForm() 
        return context
    # -----------------------------------


# 3. CREATE: Allow authenticated users to create a new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post-list') # Using 'post-list' from Task 2 fix

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Your post has been created successfully!")
        return super().form_valid(form)

# 4. UPDATE: Allow post authors to edit their posts
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

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
    success_url = reverse_lazy('post-list') # Using 'post-list' from Task 2 fix
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author 
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Your post has been deleted successfully!")
        return super().delete(request, *args, **kwargs)


# --- Task 3: Comment Views ---

@login_required
def comment_create(request, pk):
    """Handles the creation of a new comment on a specific post."""
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Your comment has been posted successfully!")
            return redirect('post-detail', pk=post.pk)
    
    return redirect('post-detail', pk=post.pk)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Allows comment author to edit their comment."""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    context_object_name = 'comment'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def form_valid(self, form):
        messages.success(self.request, "Your comment has been updated successfully.")
        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Allows comment author to delete their comment."""
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    context_object_name = 'comment'
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Your comment has been deleted successfully.")
        return super().delete(request, *args, **kwargs)
