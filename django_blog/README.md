# 💻 ALX Django LearnLab: Comprehensive Blog Project

This repository hosts a multi-stage Django project designed to build a fully functional blogging platform, adhering to industry best practices, including the use of PostgreSQL and environment variables for security.

## Task 0: Initial Setup and Project Configuration (Completed)

This task established the foundational structure for the entire project, focusing on professional setup, security, and correct file organization.

### 🛠️ Key Technologies & Setup Decisions

* **Framework:** Django 5.x
* **Database:** PostgreSQL (configured for production-readiness).
* **Security:** Sensitive data is stored in a **.env** file, which is protected using `.gitignore`.
* **Database Model:** The foundational `Post` model has been defined and migrated to PostgreSQL.
* **Template Structure:** Project uses a project-level `base.html` in the `templates/` directory for universal layout.

---
---

## Task 1: Implementing the Blog's User Authentication System (Completed)

Objective: Develop a comprehensive user authentication system for your Django blog project, enabling user registration, login, logout, and profile management.

### 📝 Implementation Details

* **Custom Form (`blog/forms.py`):** The `CustomUserCreationForm` extends Django's base form to ensure the **email field** is collected during registration, allowing for richer user profiles.
* **Built-in Views:** Django's `LoginView` and `LogoutView` are used directly in `blog/urls.py` for standard handling of these processes, which includes automatic password hashing and session management.
* **Custom Views (`blog/views.py`):**
    * `register`: Handles the custom registration form submission and uses Django's `messages` framework for feedback.
    * `profile`: Uses the `@login_required` decorator to protect access. It allows authenticated users to view and update their email address.
* **Security:** All forms automatically include CSRF tokens via the `{% csrf_token %}` template tag. Passwords are handled securely by Django's hashing algorithms.

### 🧪 How to Test

1.  **Register:** Navigate to `/register`. Fill out the username, email, and password. Submit the form. You should be redirected to the `/login` page with a success message.
2.  **Login:** Navigate to `/login`. Use the credentials from your registration. Successful login redirects you to the home page (`/`). The navigation header should now show "Profile" and "Logout".
3.  **Profile Management:** After logging in, navigate to `/profile`. You can view your username and edit your email address. Submit the form to see a success message.
4.  **Logout:** Click the "Logout" link in the navigation bar. You should be redirected to the home page, and the header links will revert to "Login" and "Register".

---

### 🚀 Setup and Running Instructions (Task 0 Remainder)

1.  **Clone the Repository and Activate Environment:**
    ```bash
    git clone [REPO_URL]
    cd django_blog
    source .venv/bin/activate
    ```
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure Environment:**
    * Edit the **.env** file and replace the placeholder values for `SECRET_KEY`, database credentials, etc., with your secure credentials (e.g., DB_USER=fidelis).
    * Ensure your **PostgreSQL** server is running and the necessary user/database are created.
4.  **Run Migrations:**
    ```bash
    python manage.py migrate
    ```
5.  **Start Server:**
    ```bash
    python manage.py runserver
    ```
    Access the blog at `http://127.0.0.1:8000/`.
