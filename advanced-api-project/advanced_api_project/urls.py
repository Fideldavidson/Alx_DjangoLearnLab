from django.contrib import admin
from django.urls import path
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Author, Book
from api.serializers import AuthorSerializer, BookSerializer

class AuthorListAPIView(APIView):
    def get(self, request):
        authors = Author.objects.all()
        return Response(AuthorSerializer(authors, many=True).data)

class BookListCreateAPIView(APIView):
    def get(self, request):
        books = Book.objects.all()
        return Response(BookSerializer(books, many=True).data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authors/', AuthorListAPIView.as_view(), name='authors'),
    path('books/', BookListCreateAPIView.as_view(), name='books'),
]
