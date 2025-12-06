from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import UpdateView, DeleteView
from .models import Post, Comment
from .forms import CommentForm

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect("post-detail", pk=post.pk)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comments_form.html"

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        return self.get_object().author == self.request.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comments_confirm_delete.html"

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        return self.get_object().author == self.request.user
# Inject CommentForm into PostDetailView context
try:
    from django.views.generic import DetailView
    from .forms import CommentForm as _CommentFormAlias
    class PostDetailView(DetailView):  # if already defined, manually add get_context_data instead of duplicating class
        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["form"] = _CommentFormAlias()
            return context
except Exception:
    pass
