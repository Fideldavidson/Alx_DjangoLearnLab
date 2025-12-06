from .views import add_comment, CommentUpdateView, CommentDeleteView

urlpatterns += [
    path("post/<int:pk>/comments/new/", add_comment, name="comment-create"),
    path("comments/<int:pk>/edit/", CommentUpdateView.as_view(), name="comment-update"),
    path("comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"),
]
