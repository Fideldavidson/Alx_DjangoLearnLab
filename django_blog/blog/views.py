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

from .forms import CustomUserCreationForm, PostForm, CommentForm
from .models import Post, Comment
from django.utils import timezone


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

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date'] 

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm() 
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Your post has been created successfully!")
        return super().form_valid(form)

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

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author 
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Your post has been deleted successfully!")
        return super().delete(request, *args, **kwargs)


# --- Task 3: Comment Views ---

# 1. Comment Create View (CBV Compliant)
class CommentCreateView(LoginRequiredMixin, CreateView):
    """Handles the creation of a new comment on a specific post."""
    model = Comment
    form_class = CommentForm
    
    def form_valid(self, form):
        # 1. Get the post ID from the URL (pk in our url pattern is the post's pk)
        post_pk = self.kwargs['pk']
        post = get_object_or_404(Post, pk=post_pk)
        
        # 2. Set the post and author
        comment = form.save(commit=False)
        comment.post = post
        comment.author = self.request.user
        comment.save()

        messages.success(self.request, "Your comment has been posted successfully!")
        
        # 3. Redirect back to the post detail page
        return redirect('post-detail', pk=post.pk)


# 2. Comment Update View
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
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


# 3. Comment Delete View
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'
    context_object_name = 'comment'
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Your comment has been deleted successfully.")
        return super().delete(request, *args, **kwargs)

from django.db.models import Q # <-- NEW IMPORT for Search

# --- Task 4: Tagging and Search Views ---

class PostTagListView(ListView):
    """Displays a list of posts filtered by a specific tag."""
    model = Post
    template_name = 'blog/post_list.html' # Reuse the existing list template
    context_object_name = 'posts'
    
    def get_queryset(self):
        # Filter posts where the tag__slug matches the slug provided in the URL
        return Post.objects.filter(tags__slug=self.kwargs.get('tag_slug')).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_slug'] = self.kwargs.get('tag_slug')
        context['tag_name'] = self.kwargs.get('tag_slug').replace('-', ' ').title()
        return context


class SearchResultsListView(ListView):
    """Displays search results based on title, content, or tags."""
    model = Post
    template_name = 'blog/search_results.html' # New template for results
    context_object_name = 'results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            # Use Q objects to perform OR search across multiple fields
            queryset = Post.objects.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query) # Search by tag name
            ).distinct().order_by('-published_date')
            return queryset
        return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context
