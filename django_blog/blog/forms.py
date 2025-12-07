from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 
from .models import Post # <-- THIS IS THE MISSING IMPORT

class CustomUserCreationForm(UserCreationForm):
    """
    Extends the default UserCreationForm to include the email field.
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        field_classes = {
            'email': forms.EmailField,
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure email is required
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(username=self.cleaned_data.get('username')).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

class PostForm(forms.ModelForm):
    """
    ModelForm for creating and updating Post objects.
    """
    class Meta:
        model = Post # <-- Now correctly defined
        # Exclude the author and published_date fields, 
        # as they will be set automatically in the views.
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter post title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10, 'placeholder': 'Write your content here...'}),
        }
