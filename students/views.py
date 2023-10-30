from django import urls
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.contrib.auth.decorators import login_required
from .models import *
from librarians.models import *
from datetime import datetime, timedelta


# Create your views here.
def index(request):
    return render(request, '.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            user_login(request, user)
            return redirect(urls.reverse('student_dashboard'))
    return render(request, 'students/login.html')

def logout(request):
    user_logout(request)
    return redirect(urls.reverse('student_login'))


def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        roll_number = request.POST.get('roll_no')
        branch = request.POST.get('branch')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        profile = request.FILES.get('profile')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password != confirm_password:
            print("passwords didn't match")
            messages.add_message(request, messages.ERROR, "Passwords didn't match")
            return redirect(urls.reverse('student_registration'))
        
        new_user = User()
        new_user.username = username
        new_user.set_password(password)
        new_user.save()

        Student.objects.create(
            username = username,
            name = name,
            roll_number = roll_number,
            branch = branch,
            mobile = mobile,
            email = email,
            profile = profile,
            user_id = new_user.id
        )
        messages.add_message(request, messages.SUCCESS, "Registered Successfully")
    return render(request, 'students/registration.html')

@login_required(login_url='/student/login/')
def dashboard(request):
    user = Student.objects.get(user_id = request.user.id)
    issued_books = IssuedBook.objects.filter(student_roll_number = user.roll_number)
    books = []
    for book in issued_books:
        book_name = Book.objects.get(isbn = book.isbn).name
        if datetime.date(datetime.today()) < book.expiry_date:
            fine = 0
        else:
            delta = datetime.date(datetime.today()) - book.expiry_date
            fine = delta.days * 5
        books.append(
            {
                'name' : book_name,
                'isbn' : book.isbn,
                'issued_date' : book.issued_date,
                'expiry_date' : book.expiry_date,
                'fine' : fine
            }
        )
    return render(request, 'students/dashboard', {'books' : books})

@login_required(login_url='/student/login/')
def change_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            user = request.user
            user.set_password(password)
            user.save()
    return render(request, 'students/change_password.html')