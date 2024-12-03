from django.urls import path
from . import views
from .views import contact_librarian
from .views import edit_news, news_details, delete_news
urlpatterns = [
    path('about/', views.about_library_for_user, name='about_library_for_user'),
    path('news/<int:id>/edit/', edit_news, name='news_edit'),
    path('news/<int:pk>/', news_details, name='news_details'),
    path('news/<int:id>/delete/', delete_news, name='news_delete'),
    path('news/add/', views.add_news, name='add_news'),
    path('news/<int:id>/edit/', views.edit_news, name='news_edit'),
    path('news/<int:id>/delete/', views.delete_news, name='news_delete'),
    path('news/<int:id>/', views.news_details, name='news_details'),
    path('contact_librarian', contact_librarian, name='contact_librarian'),
    # Головна сторінка (Landing Page)
    path('', views.landing_page, name='landing'),
    path('readers/', views.readers, name='readers'),
    path('readers/add/', views.save_reader, name='save_reader'),
    # Вхід для бібліотекаря
    path('login/librarian/', views.librarian_login, name='librarian_login'),
    path('news/<int:pk>/', views.news_details_for_user, name='news_details'),

    path('news_details/<int:pk>/', views.news_details, name='news_details'),
    path('news_details_for_user/<int:pk>/', views.news_details_for_user, name='news_details_for_user'),

    # Головна сторінка після входу
    path('home/', views.home, name='home'),
    path('home_for_user/', views.home_for_user, name='home_for_user'),
    path('news_for_user/<int:pk>/', views.news_details_for_user, name='news_details_for_user'),

    # Доступ тільки для бібліотекаря
    path('books/add/', views.add_book, name='add_book'),  # Додавання книги
    path('readers/', views.readers_tab, name='readers_tab'),  # Перегляд читачів
    path('readers/add/', views.save_reader, name='add_reader'),  # Додавання читача
    path('returns/', views.returns_page, name='returns'),  # Сторінка повернення книг

    # Доступ для всіх (читачів і бібліотекарів)
    path('books/', views.books, name='books'),  # Сторінка книг
    path('books/<int:id>/', views.book_details, name='book_details'),  # Деталі книги
    path('news/add/', views.add_news, name='add_news'),  # Додавання новини
    # Сторінка для користувача
    path('index_for_user/', views.index_for_user, name='index_for_user'),  # Сторінка для користувача

    # Додаткові маршрути для редагування/видалення книг
    path('books/<int:id>/edit/', views.edit_book, name='edit_book'),  # Редагування книги
    path('books/<int:id>/delete/', views.delete_book, name='delete_book'),  # Видалення книги

    # Вхід для користувача
    path('login/user/', views.user_login, name='user_login'),  # Вхід для користувача

    # Додаткові маршрути для користувача
    path('books_search_for_user/', views.books_search_for_user, name='books_search_for_user'),  # Пошук книг,
    path('books_details_for_user/<int:id>/', views.books_details_for_user, name='books_details_for_user'),

    path('news/', views.news_list, name='news_list'),
    path('return_for_user/', views.return_for_user, name='return_for_user'),  # Повернення книги для користувача
    path('read_news_for_user/', views.read_news_for_user, name='read_news_for_user'),  # Читання новин для користувача
]
