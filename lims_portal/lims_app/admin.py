# lims_app/admin.py

from django.contrib import admin
from .models import Reader  # Імпортуйте вашу модель reader
from .models import Book
admin.site.register(Reader)  # Реєструємо модель reader в адмінці

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'genre', 'available')
    search_fields = ('title', 'author', 'isbn')
