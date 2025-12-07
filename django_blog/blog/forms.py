from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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

    # Note: Django's built-in User model already has username, email, and password.
    # The clean_email method ensures uniqueness, which is good practice.
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exclude(username=self.cleaned_data.get('username')).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

