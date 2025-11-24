from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# List all books (read-only, open to everyone)
class BookListView(generics.ListAPIView):
    """
    Retrieves all books.
    Accessible to unauthenticated users (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# Retrieve a single book by ID (read-only, open to everyone)
class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieves a single book by ID.
    Accessible to unauthenticated users (read-only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


# Create a new book (restricted to authenticated users)
class BookCreateView(generics.CreateAPIView):
    """
    Creates a new book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Custom behavior: ensure validation runs and save
        serializer.is_valid(raise_exception=True)
        serializer.save()


# Update an existing book (restricted to authenticated users)
class BookUpdateView(generics.UpdateAPIView):
    """
    Updates an existing book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Custom behavior: ensure validation runs and save
        serializer.is_valid(raise_exception=True)
        serializer.save()


# Delete a book (restricted to authenticated users)
class BookDeleteView(generics.DestroyAPIView):
    """
    Deletes a book.
    Restricted to authenticated users.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
