from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from .models import Post

# Login form
class BlogLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput
    )

# Registration form
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

# Profile update form
class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

# Blog post form
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
