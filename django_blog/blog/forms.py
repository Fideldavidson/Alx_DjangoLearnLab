from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Comment

# --- Task 1: Custom Registration Form ---
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

# --- Task 2 & 4: Post Management Form ---
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # Ensure 'tags' is included in the fields list
        fields = ['title', 'content', 'tags'] # <-- UPDATED for Tagging
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'tags': 'Tags (comma separated)', # Helpful label for users
        }

# --- Task 3: Comment Form ---
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your comment here...'}),
        }
