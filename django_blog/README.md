# 💻 ALX Django LearnLab: Comprehensive Blog Project

This repository hosts a multi-stage Django project designed to build a fully functional blogging platform. Each task focuses on a specific set of Django features, adhering to industry best practices, including the use of PostgreSQL and environment variables for security.

## Task 0: Initial Setup and Project Configuration (Mandatory)

This task established the foundational structure for the entire project, focusing on professional setup, security, and correct file organization.

### 🛠️ Key Technologies & Setup Decisions

* **Framework:** Django 5.x
* **Database:** PostgreSQL (configured for production-readiness).
* **Dependencies:** `psycopg2-binary` (PostgreSQL adapter) and `django-environ` (for secure configuration).
* **Security:** Sensitive data (`SECRET_KEY`, database credentials) are stored in a **.env** file, which is protected using `.gitignore`.
* **Template Structure:** Project uses a **project-level `base.html`** in the `templates/` directory for universal layout, minimizing code duplication across apps.
* **Static Files:** CSS (`styles.css`) and JS (`scripts.js`) are served from the project-level `static/` directory, linked via `STATICFILES_DIRS`.

---

### 📂 Project Structure Overview

django_blog/ ├── .env <-- Environment variables (IGNORED) ├── .gitignore <-- Specifies files/dirs to ignore ├── manage.py <-- Django command-line utility ├── requirements.txt <-- Project dependencies ├── static/ <-- Project-wide static files (CSS/JS) │ ├── css/ │ └── js/ ├── templates/ <-- Project-wide templates │ └── base.html <-- Base layout template, extends to all apps ├── django_blog/ <-- Main project configuration │ ├── settings.py <-- Reads secrets/DB config from .env │ └── urls.py <-- Main URL dispatcher └── blog/ <-- Primary application for blogging logic ├── models.py <-- Defines the Post model ├── templates/blog/ <-- App-specific content templates (e.g., home.html) ├── urls.py <-- App URL configuration └── views.py <-- Initial view logic (home, post_list placeholder)


---

### ⚙️ Database Model (`blog/models.py`)

The foundational `Post` model has been defined and migrated to PostgreSQL:

| Field | Type | Description |
| :--- | :--- | :--- |
| `title` | `CharField(200)` | The title of the post. |
| `content` | `TextField` | The full body of the post. |
| `published_date` | `DateTimeField` | Automatically set on creation (`auto_now_add=True`). |
| `author` | `ForeignKey(User)` | Links the post to a Django `User` model, with `on_delete=CASCADE`. |

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
    * **Crucially:** Edit the **.env** file and replace the placeholder values for `SECRET_KEY`, `DB_USER`, and `DB_PASSWORD` with your secure credentials.
    * Ensure your **PostgreSQL** server is running and the database specified in `.env` (`django_blog_db`) is created.
4.  **Run Migrations:**
    ```bash
    python manage.py migrate
    ```
5.  **Start Server:**
    ```bash
    python manage.py runserver
    ```
    Access the blog at `http://127.0.0.1:8000/`.
