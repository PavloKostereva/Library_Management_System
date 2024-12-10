
from django.contrib import admin
from .models import Reader, Book, News  # Імпортуємо моделі

admin.site.register(Reader)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'genre', 'available')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('available', 'genre')  # Додано фільтри для кращої навігації
    actions = ['delete_selected']  # Додаємо можливість видаляти книги

    # Визначення дії для видалення вибраних книжок
    def delete_selected(self, request, queryset):
        # Додаткові перевірки перед видаленням (якщо потрібно)
        queryset.delete()
    delete_selected.short_description = "Видалити вибрані книги"  # Текст для дії

# Реєструємо BookAdmin
admin.site.register(Book, BookAdmin)

# Налаштовуємо адмінку для моделі News
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')  # Відображаємо основні поля
    search_fields = ('title',)  # Додаємо пошук за заголовком
    actions = ['delete_selected']  # Додаємо можливість видаляти новини

    # Дія для видалення вибраних новин
    def delete_selected(self, request, queryset):
        queryset.delete()
    delete_selected.short_description = "Видалити вибрані новини"  # Текст для дії

# Реєструємо NewsAdmin
admin.site.register(News, NewsAdmin)
