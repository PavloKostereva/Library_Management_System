from django.http import HttpResponse
from datetime import timedelta
from .models import Reader, Return
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from .models import Book
from django.db.models import Q
from .models import News
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import ctypes

def get_book_return_details(request):
    # Завантаження DLL
    lib = ctypes.CDLL('./ConsoleApplication3.dll')

    # Встановлення типу повернення
    lib.formatBookReturnDetails.restype = ctypes.c_char_p

    # Виклик функції
    result = lib.formatBookReturnDetails(
        b"John Doe", b"Python 101", b"2024-12-01", b"2024-12-05", True, ctypes.c_double(5.75)
    )

    # Передача результату в шаблон
    return render(request, 'book_return.html', {'book_return_details': result.decode('utf-8')})

def about_library_for_user(request):
    return render(request, 'about_library_for_user.html', {"current_tab": "about"})


def home(request):
    return render(request, 'home.html', context={"current_tab": "home"})

def home_for_user(request):
    return render(request, 'home_for_user.html')
@login_required
def books_search_for_user(request):
    query = request.GET.get('query', '')
    user_books = []

    if query:
        user_books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query) |
            Q(genre__icontains=query)
        )
    else:
        user_books = Book.objects.all()

    return render(request, 'books_search_for_user.html', {'books': user_books, 'query': query})


def return_for_user(request):
    return render(request, 'return_for_user.html')

def read_news_for_user(request):
    news_list = News.objects.all().order_by('-created_at')  # Отримуємо всі новини
    return render(request, 'read_news_for_user.html', {'news_list': news_list})

def index_for_user(request):
    # Логіка для відображення сторінки для користувача
    return render(request, 'home_for_user.html')
def readers_admin(request):
    return render(request, 'readers_admin.html')


def readers(request):
    query = request.GET.get('query', '')  # Отримуємо запит для пошуку
    if query:
        readers = Reader.objects.filter(
            Q(reader_name__icontains=query) |
            Q(reader_contact__icontains=query) |
            Q(reference_id__icontains=query)
        )
    else:
        readers = Reader.objects.all()  # Якщо немає запиту, виводимо всіх читачів
    return render(request, 'readers.html', {'readers': readers, 'query': query})


@login_required
def readers_tab(request):
    if not request.user.is_staff:
        return HttpResponse("Доступ заборонено. Ця сторінка доступна тільки бібліотекарям.", status=403)
    readers = Reader.objects.all()
    return render(request, 'readers.html', {'readers': readers, 'current_tab': 'readers'})



def books_tab(request):
    if not request.user.is_staff:  # Перевірка, чи користувач є бібліотекарем
        return HttpResponse("Доступ заборонено. Ця сторінка доступна тільки бібліотекарям.", status=403)

    # Ваш код для обробки запиту і відображення списку книг
    books = Book.objects.all()
    return render(request, 'books_and_add.html', {'books': books})
def save_reader(request):
    if request.method == 'POST':
        reference_id = request.POST.get('reader_ref_id', '')
        if Reader.objects.filter(reference_id=reference_id).exists():
            return HttpResponse("Користувач із таким ID вже існує", status=400)

        reader_item = Reader(
            reader_name=request.POST.get('reader_name', ''),
            reader_contact=request.POST.get('reader_contact', ''),
            reference_id=reference_id,
            reader_address=request.POST.get('address', ''),
            active=True
        )
        reader_item.save()
        return redirect('/readers')

    return HttpResponse("Невірний метод запиту", status=400)


def books(request):
    query = request.POST.get('query', '')  # Отримуємо запит для пошуку
    if query:
        books = Book.objects.filter(
            title__icontains=query
        ) | Book.objects.filter(
            author__icontains=query
        ) | Book.objects.filter(
            genre__icontains=query
        )
    else:
        books = Book.objects.all()  # Якщо немає запиту, виводимо всі книги

    # Перевірка ролі користувача
    if request.user.is_staff:  # Якщо бібліотекар
        can_add_book = True
    else:  # Якщо користувач
        can_add_book = False

    return render(request, 'books_and_add.html', {'books': books, 'query': query, 'can_add_book': can_add_book})

def login_reader(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        reference_id = request.POST.get('reference_id', '')

        # Перевірка існування користувача
        try:
            reader = Reader.objects.get(reader_name=name, reference_id=reference_id, active=True)
            request.session['reader_id'] = reader.id  # Зберігаємо ID у сесії
            return redirect('/dashboard')  # Перенаправлення на головну сторінку користувача
        except Reader.DoesNotExist:
            return HttpResponse("Користувача не знайдено. Перевірте дані або зверніться до бібліотекаря.", status=404)

    return render(request, 'user_login.html')

@login_required
def add_book(request):
    if not request.user.is_staff:
        return redirect('login:librarian')  # Redirect to login page for librarian if user is not a librarian

    if request.method == 'POST':
        title = request.POST.get('book_title')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        genre = request.POST.get('genre')
        publisher = request.POST.get('publisher')

        if title and author and isbn:
            Book.objects.create(
                title=title,
                author=author,
                isbn=isbn,
                genre=genre,
                publisher=publisher,
                added_by=request.user  # Use logged-in user as the book's creator
            )
            return redirect('books')

    return render(request, 'books_and_add.html')


def book_details(request, id):
    book = get_object_or_404(Book, id=id)
    return render(request, 'book_details.html', {'book': book})

def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect('books')

def edit_book(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        book.title = request.POST.get('title', book.title)
        book.author = request.POST.get('author', book.author)
        book.genre = request.POST.get('genre', book.genre)
        book.publisher = request.POST.get('publisher', book.publisher)
        book.description = request.POST.get('description', book.description)
        book.save()
        return redirect('book_details', id=book.id)
    return render(request, 'edit_book.html', {'book': book})

def returns_page(request):
    if request.method == 'GET':
        returns = Return.objects.all()
        return render(request, 'returns.html', context={'returns': returns})
    elif request.method == 'POST':
        query = request.POST.get('query', '')
        filtered_returns = Return.objects.filter(
            book__title__icontains=query
        ) | Return.objects.filter(
            book__author__icontains=query
        ) | Return.objects.filter(
            reader__reader_name__icontains=query
        )
        return render(request, 'returns.html', context={'returns': filtered_returns, 'query': query})

def check_return_status(request, return_id):
    try:
        return_item = Return.objects.get(id=return_id)
        data = {
            "book_title": return_item.book.title,
            "reader_name": return_item.reader.reader_name,
            "return_date": return_item.return_date,
            "is_overdue": return_item.is_overdue,
            "fine": return_item.fine,
        }
        return JsonResponse(data)
    except Return.DoesNotExist:
        return JsonResponse({"error": "Return record not found"}, status=404)

def extend_return(request, return_id):
    try:
        return_item = Return.objects.get(id=return_id)
        if return_item.book.is_reserved:
            return JsonResponse({"error": "The book is reserved by another user. Extension not possible."}, status=400)
        return_item.due_date += timedelta(days=7)
        return_item.save()
        return JsonResponse({"message": "Return period successfully extended!"})
    except Return.DoesNotExist:
        return JsonResponse({"error": "Return record not found"}, status=404)

@csrf_exempt  # Якщо є проблеми з CSRF, але краще налаштувати токен
def contact_librarian(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if name and email and message:
            try:
                send_mail(
                    subject=f"Message from {name}",
                    message=message,
                    from_email=email,
                    recipient_list=["logikasun@gmail.com"],  # Ваш email
                    fail_silently=False,
                )
                return JsonResponse({"success": True})
            except Exception as e:
                print(f"Error: {e}")
                return JsonResponse({"success": False, "error": str(e)})
        return JsonResponse({"success": False, "error": "Missing fields"})
    return JsonResponse({"success": False, "error": "Invalid request method"})
def save_student(request):
    # Ваша логіка для збереження студента
    return HttpResponse("Student saved!")

def returns_view(request):
    return render(request, 'returns.html')





def news_list(request):
    news = News.objects.all().order_by('-created_at')  # Отримання новин
    return render(request, 'news_list.html', {'news_list': news, 'current_tab': 'news'})




def librarian_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('home')  # Перенаправити на сторінку HOME
        else:
            return render(request, 'librarian_login.html', {'error': 'Невірні дані'})
    return render(request, 'librarian_login.html')


def user_login(request):
    if request.method == 'POST':
        # Отримуємо введені ім'я та ID
        name = request.POST.get('name')
        reference_id = request.POST.get('reference_id')

        # Перевірка, чи співпадає ім'я та ID
        if name == "Pavlo" and reference_id == "12345":
            # Якщо ім'я та ID правильні, перенаправляємо користувача на сторінку для користувача
            return redirect('index_for_user')  # Замість 'home' вказуємо 'index_for_user'
        else:
            # Якщо ім'я або ID невірні, показуємо помилку
            return HttpResponse("Невірне ім'я або ID!")

    return render(request, 'user_login.html')


def books_details_for_user(request, id):
    book = get_object_or_404(Book, id=id)
    return render(request, 'books_details_for_user.html', {'book': book})


def user_dashboard(request):
    if 'reader_id' not in request.session:  # Перевірка наявності сесії користувача
        return redirect('user_login')
    reader_instance = get_object_or_404(Reader, id=request.session['reader_id'])
    return render(request, 'user_dashboard.html', {'reader': reader_instance})



@login_required
def librarian_dashboard(request):
    if not request.user.is_staff:
        return redirect('/login/librarian/')
    return render(request, 'librarian_dashboard.html')

def news_details_for_user(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news_details_for_user.html', {'news': news})


def news_details(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news_details.html', {'news': news})
@login_required
def read_news(request):
    news_list = News.objects.all().order_by('-created_at')  # Отримуємо всі новини
    return render(request, 'read_news.html', {'news_list': news_list})  # Повертаємо список новин

def landing_page(request):
    return render(request, 'landing.html')

def add_news(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        news = News.objects.create(title=title, content=content)
        return JsonResponse({'success': True, 'title': news.title, 'content': news.content, 'id': news.id})
    return render(request, 'add_news.html')

def edit_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    if request.method == 'POST':
        news.title = request.POST.get('title')
        news.content = request.POST.get('content')
        news.save()
        return JsonResponse({'success': True, 'title': news.title, 'content': news.content, 'id': news.id})
    return render(request, 'edit_news.html', {'news': news})

def delete_news(request, news_id):
    news = get_object_or_404(News, id=news_id)
    news.delete()
    return JsonResponse({'success': True})