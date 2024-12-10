import ctypes
from ctypes import c_char_p, c_int, c_double, c_void_p
from typing import List, Dict

# Завантаження DLL
dll = ctypes.CDLL("C:\Users\Admin\PycharmProjects\Library_Management_System\lims_portal\inventory.dll")



class Book(ctypes.Structure):
    _fields_ = [
        ("title", c_char_p),
        ("author", c_char_p),
        ("genre", c_char_p),
        ("publisher", c_char_p),
    ]

class User(ctypes.Structure):
    _fields_ = [
        ("name", c_char_p),
        ("reference_id", c_char_p),
    ]

# Функція CreateBook
dll.CreateBook.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p]
dll.CreateBook.restype = Book

def create_book(title: str, author: str, genre: str, publisher: str) -> Book:
    return dll.CreateBook(title.encode('utf-8'), author.encode('utf-8'),
                          genre.encode('utf-8'), publisher.encode('utf-8'))

# Функція DeleteBook
dll.DeleteBook.argtypes = [ctypes.POINTER(Book), c_char_p]
dll.DeleteBook.restype = None

def delete_book(books: List[Book], title: str) -> None:
    arr = (Book * len(books))(*books)
    dll.DeleteBook(arr, title.encode('utf-8'))

# Функція SearchBooks
dll.SearchBooks.argtypes = [ctypes.POINTER(Book), c_char_p]
dll.SearchBooks.restype = ctypes.POINTER(Book)

def search_books(books: List[Book], query: str) -> List[Book]:
    arr = (Book * len(books))(*books)
    result = dll.SearchBooks(arr, query.encode('utf-8'))
    return [result[i] for i in range(len(books))]

# Функція CountBooksByGenre
dll.CountBooksByGenre.argtypes = [ctypes.POINTER(Book), c_char_p]
dll.CountBooksByGenre.restype = c_int

def count_books_by_genre(books: List[Book], genre: str) -> int:
    arr = (Book * len(books))(*books)
    return dll.CountBooksByGenre(arr, genre.encode('utf-8'))

# Функція CreateUser
dll.CreateUser.argtypes = [c_char_p, c_char_p]
dll.CreateUser.restype = User

def create_user(name: str, reference_id: str) -> User:
    return dll.CreateUser(name.encode('utf-8'), reference_id.encode('utf-8'))

# Функція ValidateUser
dll.ValidateUser.argtypes = [User, c_char_p, c_char_p]
dll.ValidateUser.restype = ctypes.c_bool

def validate_user(user: User, name: str, reference_id: str) -> bool:
    return dll.ValidateUser(user, name.encode('utf-8'), reference_id.encode('utf-8'))

# Функція GetCurrentDate
dll.GetCurrentDate.argtypes = []
dll.GetCurrentDate.restype = c_char_p

def get_current_date() -> str:
    return dll.GetCurrentDate().decode('utf-8')

# Функція CalculateDaysBetween
dll.CalculateDaysBetween.argtypes = [c_char_p, c_char_p]
dll.CalculateDaysBetween.restype = c_int

def calculate_days_between(date1: str, date2: str) -> int:
    return dll.CalculateDaysBetween(date1.encode('utf-8'), date2.encode('utf-8'))

# Функція CreateNews
class News(ctypes.Structure):
    _fields_ = [
        ("title", c_char_p),
        ("content", c_char_p),
    ]

dll.CreateNews.argtypes = [c_char_p, c_char_p]
dll.CreateNews.restype = News

def create_news(title: str, content: str) -> News:
    return dll.CreateNews(title.encode('utf-8'), content.encode('utf-8'))
