from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.detail import DetailView
from .models import Book, Library, UserProfile


def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


def admin_check(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def librarian_check(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def member_check(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


@user_passes_test(admin_check)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(librarian_check)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


@user_passes_test(member_check)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')