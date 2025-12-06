# Django Blog Authentication System

## Overview
This authentication system enables user registration, login, logout, and profile management. It builds on Django’s built-in authentication framework and custom forms.

## Features
- **Registration**: Users can create accounts with username, email, and password.
- **Login/Logout**: Secure login and logout using Django’s built-in views.
- **Profile Management**: Authenticated users can view and update their username and email.
- **Messages**: Success/error feedback displayed on all forms.
- **Security**: CSRF protection, password hashing, and `login_required` decorators.

## URLs
- `/register` → Registration page
- `/login` → Login page
- `/logout` → Logout confirmation
- `/profile` → Profile management (requires login)
- `/` → Homepage
- `/posts` → Placeholder blog posts page

## Templates
- `login.html` → Login form
- `logout.html` → Logout confirmation
- `register.html` → Registration form
- `profile.html` → Profile management
- `home.html` → Homepage
- `posts.html` → Placeholder for blog posts

## Forms
- `RegisterForm` → Extends `UserCreationForm` with email field.
- `ProfileForm` → Allows editing username and email.

## Views
- `BlogLoginView` → Handles login.
- `BlogLogoutView` → Handles logout.
- `register()` → Handles registration.
- `profile()` → Handles profile management.
- `home()` → Homepage.
- `posts()` → Placeholder blog posts.

## Testing Instructions
1. **Register**: Go to `/register`, create a new account.
2. **Login**: Go to `/login`, enter credentials, redirected to `/profile`.
3. **Profile**: At `/profile`, edit username/email, save changes.
4. **Logout**: At `/logout`, confirm logout, redirected to `/login`.
5. **Homepage**: Visit `/` to see welcome page.
6. **Posts**: Visit `/posts` to see placeholder.

## Security Notes
- CSRF tokens included in all forms.
- Passwords securely hashed by Django.
- Profile view protected with `@login_required`.

