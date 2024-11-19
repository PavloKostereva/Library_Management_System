from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from datetime import timedelta
from .models import Book, Reader, Return
from .models import News
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Book

def home(request):
    return render(request, 'home.html', context={"current_tab": "home"})

def readers_admin(request):
    return render(request, 'readers_admin.html')



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
        reader_item = Reader(
            reader_name=request.POST.get('reader_name', ''),
            reader_contact=request.POST.get('reader_contact', ''),
            reference_id=request.POST.get('reader_ref_id', ''),
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



@login_required
def add_book(request):
    if not request.user.is_staff:  # Перевірка, чи бібліотекар
        return redirect('/login/librarian/')  # Перенаправлення на сторінку входу бібліотекаря

    if request.method == 'POST':
        title = request.POST.get('book_title')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        genre = request.POST.get('genre')
        publisher = request.POST.get('publisher')

        # Перевіряємо чи всі необхідні поля заповнені
        if title and author and isbn:
            # Створюємо нову книгу і зберігаємо її в базі даних
            Book.objects.create(
                title=title,
                author=author,
                isbn=isbn,
                genre=genre,
                publisher=publisher
            )
            return redirect('books')  # Переадресація на сторінку зі списком книг

    return render(request, 'books_and_add.html')  # Повернення до форми додавання книги

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

def contact_librarian(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        send_mail(
            subject=f"Message from {name}",
            message=message,
            from_email=email,
            recipient_list=["librarian@example.com"],
        )
        return JsonResponse({"message": "Your message has been sent!"})
    return JsonResponse({"error": "Invalid request method"}, status=400)
def save_student(request):
    # Ваша логіка для збереження студента
    return HttpResponse("Student saved!")

def returns_view(request):
    return render(request, 'returns.html')


@login_required
def add_news(request):
    if not request.user.is_staff:
        return redirect('/')  # Перенаправлення для не бібліотекарів

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:
            news_item = News(
                title=title,
                content=content
            )
            news_item.save()
            return redirect('news_list')  # Перенаправлення на сторінку зі списком новин

    news_list = News.objects.all().order_by('-created_at')  # Отримуємо всі новини
    return render(request, 'add_news.html', {'news_list': news_list})  # Повертаємо форму та список новин



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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Перенаправляємо на спільну сторінку після успішного входу
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'login.html')



def user_dashboard(request):
    if 'reader_id' not in request.session:  # Перевірка наявності сесії користувача
        return redirect('user_login')
    reader_instance = get_object_or_404(Reader, id=request.session['reader_id'])
    return render(request, 'user_dashboard.html', {'reader': reader_instance})


from django.contrib.auth.decorators import login_required

@login_required
def librarian_dashboard(request):
    if not request.user.is_staff:
        return redirect('/login/librarian/')
    return render(request, 'librarian_dashboard.html')
@login_required
def news_details(request, news_id):
    news_item = get_object_or_404(News, id=news_id)
    return render(request, 'news_details.html', {'news_item': news_item})

@login_required
def read_news(request):
    news_list = News.objects.all().order_by('-created_at')  # Отримуємо всі новини
    return render(request, 'read_news.html', {'news_list': news_list})  # Повертаємо список новин

def landing_page(request):
    return render(request, 'landing.html')


