from django.db import models
from datetime import date

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

    def __str__(self):
        return self.title

class Return(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    return_date = models.DateField(default=date.today)
    due_date = models.DateField()
    is_overdue = models.BooleanField(default=False)
    fine = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
