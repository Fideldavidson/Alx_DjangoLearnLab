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
### 🚀 Setup and Running Instructions

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
    * Edit the **.env** file and replace the placeholder values for `SECRET_KEY`, database credentials, etc., with your secure credentials.
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

---

## Task 1: Implementing the Blog's User Authentication System (Completed)

Objective: Develop a comprehensive user authentication system for your Django blog project, enabling user registration, login, logout, and profile management.

### 📝 Implementation Details

* **Custom Form (`blog/forms.py`):** The `CustomUserCreationForm` extends Django's base form to ensure the **email field** is collected during registration.
* **Built-in Views:** Django's `LoginView` and `LogoutView` are used directly in `blog/urls.py` for standard authentication processes.
* **Custom Views (`blog/views.py`):**
    * `register`: Handles the custom registration form submission.
    * `profile`: Uses the `@login_required` decorator to protect access and allows authenticated users to update their email address.
* **Security:** All forms automatically include **CSRF tokens** and passwords are handled securely by Django's built-in hashing algorithms.

### 🧪 How to Test (Task 1)

1.  **Register:** Navigate to `/register`. Submit the form and ensure you are redirected to `/login` with a success message.
2.  **Login:** Navigate to `/login`. Successful login redirects you to the home page (`/`), and the navigation header shows "Profile" and "Logout".
3.  **Profile Management:** After logging in, navigate to `/profile`. Edit your email and ensure the update is successful.
4.  **Logout:** Click the "Logout" link. The header links should revert to "Login" and "Register".

---

## Task 2: Blog Post Management Features (CRUD) (Completed)

This task implements the full Create, Read, Update, and Delete (CRUD) lifecycle for blog posts, accessible through Django's Class-Based Views (CBVs) and includes new CSS styling.

### 📝 Implementation Details

* **Views (`blog/views.py`):** Utilizes `ListView`, `DetailView`, `CreateView`, `UpdateView`, and `DeleteView`.
* **Forms (`blog/forms.py`):** The **`PostForm`** is a `ModelForm` used for post creation and editing.
* **Permissions (`Access Control`):**
    * **Create:** Protected by `LoginRequiredMixin`.
    * **Update/Delete:** Protected by both `LoginRequiredMixin` and **`UserPassesTestMixin`**, ensuring only the post author can modify or delete content.
    * **Read (List/Detail):** Accessible to all users.
* **Styling:** Custom CSS (`static/css/styles.css`) was applied to provide a clean and professional look for all forms and post views.

### 🧪 How to Test (Task 2)

1.  **View Posts (Read):** Access `/posts/`. Verify the list view is accessible to all.
2.  **Create Post (Create):** Log in and navigate to `/posts/new/`. Successfully create a post and ensure redirection works.
3.  **Edit/Delete Post (Update/Delete):** On a post you own, use the "Edit Post" and "Delete Post" links on the detail page (`/posts/<int:pk>/`). Verify the update is successful and deletion redirects to the list.
4.  **Security Check:** Attempt to access the edit/delete links for a post created by another user (or while logged out) to confirm the permission checks block access.

---

---

## Task 3: Adding Comment Functionality to Blog Posts (Completed)

Objective: Implement a full CRUD (Create, Read, Update, Delete) comment system integrated directly into the blog post detail page, ensuring proper user authentication and authorization.

### 📝 Implementation Details

* **Model (`blog/models.py`):** The `Comment` model was defined with a `ForeignKey` to `Post` and a `ForeignKey` to Django's `User` model (`author`). It uses `created_at` (default) and `updated_at` (`auto_now=True`) fields.
* **Forms (`blog/forms.py`):** A simple `CommentForm` (a `ModelForm`) was created, exposing only the `content` field.
* **Views (`blog/views.py`):**
    * **Comment Creation (Function View):** The `comment_create` function view handles form submission, automatically setting the `post` and `author` before saving, and redirecting the user back to the post detail page.
    * **Comment Display (Context):** The `PostDetailView` was updated to include an instance of `CommentForm` in its context via `get_context_data()`.
    * **Comment Management (CBVs):** `CommentUpdateView` and `CommentDeleteView` were implemented using Django's **`LoginRequiredMixin`** and **`UserPassesTestMixin`**.
* **Permissions:** The `test_func` in the update and delete CBVs strictly enforces that `self.request.user == comment.author`, ensuring users can only manage their own comments.
* **URLs (`blog/urls.py`):** URLs were configured to use an intuitive structure:
    * Creation: `/post/<int:pk>/comment/new/`
    * Management: `/comment/<int:pk>/update/` and `/comment/<int:pk>/delete/`

### 🧪 How to Test (Task 3)

1.  **Read Comments:** Access any post detail page (`/post/<int:pk>/`). The comment section should display all existing comments.
2.  **Post Comment (Create):** Log in. The comment form should be visible. Submit a comment and confirm it appears successfully below the post.
3.  **Edit/Delete (Permissions Check):**
    * As the comment author, verify the **Edit** and **Delete** links are visible on your comment.
    * Log in as a different user. Verify that you **CANNOT** see the Edit or Delete links on the first user's comment.
4.  **Edit/Delete Flow:** Successfully execute the edit and delete operations to ensure the comment system's full functionality.

---

## Task 4: Implementing Advanced Features: Tagging and Search Functionality (Completed)

Objective: Enhanced content organization and discoverability using tagging and keyword search.

### 📝 Implementation Details

* **Tagging:** Implemented using the external package `django-taggit`.
    * The `Post` model includes `tags = TaggableManager()`.
    * The `PostForm` now includes the tags field, allowing users to add comma-separated tags during creation/update.
    * **Viewing by Tag:** The `PostTagListView` filters posts based on the `tag_slug` provided in the URL.
* **Search:** Implemented using a Class-Based View, `SearchResultsListView`.
    * The search query is retrieved from the URL (`request.GET.get('q')`).
    * **Query Logic:** Django's `Q` objects are used to construct a powerful query that performs an **OR** search across `title`, `content`, and associated `tags__name`.
* **URLs:**
    * View Posts by Tag: `/tag/<slug:tag_slug>/` (uses `post-by-tag` name)
    * Search Results: `/search/` (uses `search-results` name)

### 🧪 How to Test (Task 4)

1.  **Tagging:** Create a new post and add tags (e.g., "django, tutorial, webdev"). Verify the tags appear as links on the detail page. Click a tag to ensure the `PostTagListView` correctly filters posts.
2.  **Search:** Use the new search bar in the header. Enter a title keyword, a content keyword, and a tag name. Verify all matching posts are displayed on the search results page.
