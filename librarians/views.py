from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.contrib.auth.decorators import login_required
from django import urls
from .models import *
from students.models import *
from django.contrib import messages

# Create your views here.
def home(request):
    return HttpResponse('Librarian home page') 

def logout(request):
    user_logout(request)
    return redirect(urls.reverse('librarian_login'))

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None and user.is_staff:
            user_login(request, user)
            return redirect(urls.reverse('add_book'))
    return render(request, 'librarians/login.html')

@login_required(login_url='/librarian/login/')
def add_book(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        category = request.POST.get('category')

        Book.objects.create(name = name, author=author, isbn=isbn, category=category)
    return render(request, 'librarians/add_book.html')

@login_required(login_url='/librarian/login/')
def view_books(request):
    books = Book.objects.all()
    return render(request, 'librarians/view_books.html', {'books': books})

@login_required(login_url='/librarian/login/')
def delete_book(request, id):
    book = Book.objects.get(id = id)
    book.delete()
    return redirect(urls.reverse('librarian_dashboard'))

@login_required(login_url='/librarian/login/')
def issue_book(request):
    books = Book.objects.all()
    students = Student.objects.all()
    if request.method == 'POST':
        student = request.POST.get('student')
        book = request.POST.get('book')
        s = Student.objects.get(roll_number = student)
        check = IssuedBook.objects.filter(student_roll_number = student, isbn = book)
        if not check:
            IssuedBook.objects.create (
                student_roll_number = student,
                isbn = book
            )
            messages.add_message(request, messages.SUCCESS, "Issued Successfully")
        else:
            messages.add_message(request, messages.ERROR, "Already Issued")
        return redirect(urls.reverse('issue_book'))
        
    return render(request, 'librarians/issue_book.html', {'students':students, 'books':books})

@login_required(login_url='/librarian/login/')
def issued_books(request):
    database = IssuedBook.objects.all()
    data = []
    for details in database:
        s = Student.objects.get(roll_number = details.student_roll_number)
        b = Book.objects.get(isbn = details.isbn)
        data.append(
            {
                'book_name' : b.name, 
                'isbn' : b.isbn, 
                'student_name' : s.name, 
                'roll_number' : s.roll_number,
                'delete_id' : details.id
            }
        )
    return render(request, 'librarians/issued_books.html', {'details': data})

@login_required(login_url='/librarian/login/')
def delete_issued_book(request, id):
    issued_book_record = IssuedBook.objects.get(id = id)
    issued_book_record.delete()
    return redirect(urls.reverse('issued_books'))

@login_required(login_url='/librarian/login/')
def students_list(request):
    students = Student.objects.all()
    return render(request, 'librarians/students_list.html', {'students' : students})

@login_required(login_url='/librarian/login/')
def delete_student(request, id):
    student = User.objects.get(id = id)
    roll_number = Student.objects.get(user_id = id).roll_number
    IssuedBook.objects.filter(student_roll_number = roll_number ).delete()
    student.delete()

    return redirect(urls.reverse('students_list'))
@login_required(login_url='/librarian/login/')
def change_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            user = request.user
            user.set_password(password)
            user.save()
    return render(request, 'librarians/change_password.html')