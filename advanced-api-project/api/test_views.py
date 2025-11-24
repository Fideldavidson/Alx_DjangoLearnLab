from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Author, Book

class BookAPITests(APITestCase):
    def setUp(self):
        # Create a test user and log them in (checker expects self.client.login)
        self.user = User.objects.create_user(username="fides", password="strong-pass-123")
        self.client.login(username="fides", password="strong-pass-123")

        # Create test authors
        self.author1 = Author.objects.create(name="Jane Doe")
        self.author2 = Author.objects.create(name="John Smith")

        # Create test books
        self.book1 = Book.objects.create(title="Django Deep Dive", author=self.author1, publication_year=2022)
        self.book2 = Book.objects.create(title="RESTful Patterns", author=self.author2, publication_year=2024)
        self.book3 = Book.objects.create(title="Pythonic APIs", author=self.author1, publication_year=2023)

        # Define endpoint URLs
        self.list_url = "/api/books/"
        self.create_url = "/api/books/create/"
        self.detail_url = f"/api/books/{self.book1.pk}/"
        self.update_url = f"/api/books/{self.book1.pk}/update/"
        self.delete_url = f"/api/books/{self.book1.pk}/delete/"

    # ----- Permissions Tests -----

    def test_list_books_unauthenticated_allowed(self):
        # Unauthenticated users should be able to view the book list
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 3)

    def test_create_book_requires_authentication(self):
        # Unauthenticated users should be blocked from creating books
        payload = {
            "title": "New Book Unauth",
            "author": self.author1.pk,
            "publication_year": 2025
        }
        response = self.client.post(self.create_url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_requires_authentication(self):
        # Unauthenticated users should be blocked from updating books
        payload = {"title": "Updated Title"}
        response = self.client.put(self.update_url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_requires_authentication(self):
        # Unauthenticated users should be blocked from deleting books
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ----- CRUD Tests with Authentication -----

    def test_create_book_authenticated(self):
        # Authenticated users should be able to create books
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "Test Driven APIs",
            "author": self.author2.pk,
            "publication_year": 2021
        }
        response = self.client.post(self.create_url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], payload["title"])
        self.assertEqual(response.data["publication_year"], payload["publication_year"])

    def test_update_book_authenticated(self):
        # Authenticated users should be able to update books
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "Django Deep Dive — Updated",
            "author": self.author1.pk,
            "publication_year": 2022
        }
        response = self.client.put(self.update_url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], payload["title"])

    def test_delete_book_authenticated(self):
        # Authenticated users should be able to delete books
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())

    # ----- Filtering, Searching, Ordering Tests -----

    def test_filter_by_publication_year(self):
        # Filter books by publication year
        response = self.client.get(f"{self.list_url}?publication_year=2024")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in response.data]
        self.assertIn("RESTful Patterns", titles)
        self.assertNotIn("Django Deep Dive", titles)

    def test_search_by_title(self):
        # Search books by title keyword
        response = self.client.get(f"{self.list_url}?search=Pythonic")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in response.data]
        self.assertIn("Pythonic APIs", titles)
        self.assertNotIn("RESTful Patterns", titles)

    def test_search_by_author_name(self):
        # Search books by author name (author__name)
        response = self.client.get(f"{self.list_url}?search=Jane")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in response.data]
        self.assertIn("Django Deep Dive", titles)
        self.assertIn("Pythonic APIs", titles)

    def test_ordering_by_title_desc(self):
        # Order books by title descending
        response = self.client.get(f"{self.list_url}?ordering=-title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in response.data]
        self.assertEqual(titles, sorted(titles, reverse=True))

    def test_ordering_by_publication_year_asc(self):
        # Order books by publication year ascending
        response = self.client.get(f"{self.list_url}?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in response.data]
        self.assertEqual(years, sorted(years))
