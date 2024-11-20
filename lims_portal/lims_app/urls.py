from django.urls import path
from . import views

urlpatterns = [
    # Головна сторінка (Landing Page)
    path('', views.landing_page, name='landing'),

    # Вхід для бібліотекаря
    path('login/librarian/', views.librarian_login, name='librarian_login'),

    # Головна сторінка після входу
    path('home/', views.home, name='home'),
    path('home_for_user/', views.home_for_user, name='home_for_user'),

    # Доступ тільки для бібліотекаря
    path('books/add/', views.add_book, name='add_book'),  # Додавання книги
    path('readers/', views.readers_tab, name='readers_tab'),  # Перегляд читачів
    path('readers/add/', views.save_reader, name='add_reader'),  # Додавання читача
    path('returns/', views.returns_page, name='returns'),  # Сторінка повернення книг

    # Доступ для всіх (читачів і бібліотекарів)
    path('books/', views.books, name='books'),  # Сторінка книг
    path('books/<int:id>/', views.book_details, name='book_details'),  # Деталі книги
    path('news/', views.news_list, name='news_list'),  # Список новин
    path('news/<int:news_id>/', views.news_details, name='news_details'),  # Деталі новини
    path('news/add/', views.add_news, name='add_news'),  # Додавання новини

    # Сторінка для користувача
    path('index_for_user/', views.index_for_user, name='index_for_user'),  # Сторінка для користувача

    # Додаткові маршрути для редагування/видалення книг
    path('books/<int:id>/edit/', views.edit_book, name='edit_book'),  # Редагування книги
    path('books/<int:id>/delete/', views.delete_book, name='delete_book'),  # Видалення книги

    # Вхід для користувача
    path('login/user/', views.user_login, name='user_login'),  # Вхід для користувача

    path('home_for_user/', views.home_for_user, name='home_for_user'),
    path('books_search_for_user/', views.books_search_for_user, name='books_search_for_user'),
    path('return_for_user/', views.return_for_user, name='return_for_user'),
    path('read_news_for_user/', views.read_news_for_user, name='read_news_for_user'),
]
