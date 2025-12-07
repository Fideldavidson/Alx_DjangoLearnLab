from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

# Import the custom form
from .forms import CustomUserCreationForm

# --- Registration View ---
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Add a success message
            messages.success(request, f'Account created for {user.username}. You can now log in!')
            return redirect('login') # Redirect to the login page
    else:
        form = CustomUserCreationForm()
    
    # Pass the form to the template
    return render(request, 'blog/register.html', {'form': form})

# --- Profile Management View ---
@login_required # Ensures only logged-in users can access this page
def profile(request):
    if request.method == 'POST':
        # Retrieve the current user instance
        user = request.user
        
        # We allow the user to update their email
        new_email = request.POST.get('email')
        
        if new_email and new_email != user.email:
            # Basic validation to ensure email isn't taken by another user
            if User.objects.filter(email=new_email).exclude(id=user.id).exists():
                messages.error(request, "This email address is already taken by another user.")
            else:
                user.email = new_email
                user.save()
                messages.success(request, "Your profile has been updated successfully.")
                
        # Redirect to GET to prevent form resubmission
        return redirect('profile')

    # Display the profile page
    return render(request, 'blog/profile.html', {'user': request.user})

# The 'home' and 'post_list' views from Task 0 remain here (not shown in the overwrite, 
# but they are logically present in the file).

def home(request):
    return render(request, 'blog/home.html', {})

def post_list(request):
    return home(request)
