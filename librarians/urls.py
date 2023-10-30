from django.urls import path
from . import views
urlpatterns = [
    path('', views.home),
    path('home/', views.home),
    path('login/', views.login, name='librarian_login'),
    path('add_book/', views.add_book, name='add_book'),
    path('logout/', views.logout, name='librarian_logout'),
    path('books/', views.view_books, name='librarian_dashboard'),
    path('issue_book/', views.issue_book, name='issue_book'),
    path('issued_books/', views.issued_books, name='issued_books'),
    path('students', views.students_list, name='students_list'),
    path('change_password', views.change_password, name='librarian_change_password'),
    path('delete_issued_book/<id>', views.delete_issued_book, name='delete_issued_book'),
    path('delete_book/<id>', views.delete_book, name='delete_book'),
    path('delete_student/<id>', views.delete_student, name='delete_student'),

    
]
