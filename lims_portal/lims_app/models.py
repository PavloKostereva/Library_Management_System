from django.db import models
from datetime import date
from django.contrib.auth.models import User
import ctypes

# Завантаження DLL
lib = ctypes.CDLL('./ConsoleApplication3.dll')

# Встановлення типів повернення функцій
lib.isBookOverdue.restype = ctypes.c_bool
lib.formatBookReturnDetails.restype = ctypes.c_char_p

# Функція для перевірки, чи книга прострочена
def check_book_overdue(due_date, return_date):
    fine = ctypes.c_double(0.0)
    is_overdue = lib.isBookOverdue(due_date.encode('utf-8'), return_date.encode('utf-8'), ctypes.byref(fine))
    return is_overdue, fine.value

# Виклик функції для форматування детальної інформації про повернення книги
def format_return_details(reader_name, book_title, due_date, return_date, is_overdue, fine):
    result = lib.formatBookReturnDetails(
        reader_name.encode('utf-8'),
        book_title.encode('utf-8'),
        due_date.encode('utf-8'),
        return_date.encode('utf-8'),
        is_overdue,
        fine
    )
    return result.decode('utf-8')

class Reader(models.Model):
    reader_name = models.CharField(max_length=255)
    reader_contact = models.CharField(max_length=255)
    reference_id = models.CharField(max_length=100)
    reader_address = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.reader_name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    publisher = models.CharField(max_length=200, blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    available = models.BooleanField(default=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

class Return(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    return_date = models.DateField(default=date.today)
    due_date = models.DateField()
    is_overdue = models.BooleanField(default=False)
    fine = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        is_overdue, fine = check_book_overdue(str(self.due_date), str(self.return_date))
        self.is_overdue = is_overdue
        self.fine = fine
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Return: {self.book.title} by {self.reader.reader_name}"

class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
