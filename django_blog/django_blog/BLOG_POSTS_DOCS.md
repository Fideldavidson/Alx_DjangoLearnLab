# Blog Post Management (CRUD)

## Overview
This feature adds full Create, Read, Update, and Delete (CRUD) functionality for blog posts. It allows authenticated users to manage their own posts, while all users can browse and read posts.

## Features
- **ListView**: Displays all posts with title, author, and snippet.
- **DetailView**: Shows full post content.
- **CreateView**: Authenticated users can create new posts.
- **UpdateView**: Only the author can edit their post.
- **DeleteView**: Only the author can delete their post.

## URLs
- `/posts/` → List all posts
- `/posts/new/` → Create a new post
- `/posts/<int:pk>/` → View post details
- `/posts/<int:pk>/edit/` → Edit a post
- `/posts/<int:pk>/delete/` → Delete a post

## Forms
- **PostForm**: Handles title and content fields. Author is set automatically from the logged-in user.

## Templates
- `posts_list.html` → List of posts
- `posts_detail.html` → Single post view
- `posts_form.html` → Create/Edit form
- `posts_confirm_delete.html` → Delete confirmation

## Permissions
- **Public**: List and detail views accessible to everyone.
- **Authenticated users**: Can create posts.
- **Authors only**: Can edit and delete their own posts.

## Testing
1. As guest: Access list and detail views; redirected to login for create/edit/delete.
2. As logged-in user: Create a post; verify author is set correctly.
3. Edit/Delete: Only author can perform these actions.
4. Navigation links work correctly between views.

