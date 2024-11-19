from django.test import TestCase
from .models import Book

class BookTestCase(TestCase):
    def setUp(self):
        Book.objects.create(title="Test Book", author="John Doe", isbn="1234567890123")

    def test_book_creation(self):
        book = Book.objects.get(title="Test Book")
        self.assertEqual(book.author, "John Doe")
