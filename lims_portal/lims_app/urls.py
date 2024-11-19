from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),  # Головна сторінка (Landing Page)
    path('login/user/', views.user_login, name='user_login'),  # Вхід для користувача
    path('login/librarian/', views.librarian_login, name='librarian_login'),  # Вхід для бібліотекаря
    path('home/', views.home, name='home'),  # Головна сторінка після входу

    # Доступ тільки для бібліотекаря
    path('books/add/', views.add_book, name='add_book'),  # Додавання книги
    path('readers/', views.readers_tab, name='readers_tab'),  # Перегляд читачів
    path('readers/add/', views.save_reader, name='add_reader'),  # Додавання читача
    path('returns/', views.returns_page, name='returns'),  # Сторінка повернення книг

    # Доступ для всіх (читачів і бібліотекарів)
    path('books/', views.books, name='books'),  # Сторінка книг
    path('books/<int:id>/', views.book_details, name='book_details'),  # Деталі книги
    path('news/', views.news_list, name='news_list'),  # Список новин
    path('news/', views.news_list, name='read_news'),
    # Додаткові маршрути
    path('books/<int:id>/edit/', views.edit_book, name='edit_book'),  # Редагування книги
    path('books/<int:id>/delete/', views.delete_book, name='delete_book'),  # Видалення книги
    path('news/<int:news_id>/', views.news_details, name='news_details'),  # Деталі новини
    path('news/add/', views.add_news, name='add_news'),  # Додавання новини

    # path('dashboard/', views.dashboard, name='dashboard'),
]
