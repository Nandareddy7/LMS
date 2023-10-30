from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index),
    path('login/', views.login, name="student_login"),
    path('registration/', views.registration, name="student_registration"),
    path('dashboard', views.dashboard, name="student_dashboard"),
    path('logout', views.logout, name="student_logout"),
    path('change_password', views.change_password, name="student_change_password"),

    
]
