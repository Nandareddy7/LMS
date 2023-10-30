from django.db import models
from django.contrib.auth import authenticate, login, logout
from datetime import datetime, timedelta
from students.models import *


# Create your models here.
class Book(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.BigIntegerField(unique=True)
    category = models.CharField(max_length=100)

def expiry():
    return datetime.today() + timedelta(days=14)

class IssuedBook(models.Model):
    # student_id = models.ManyToManyField(Student)
    student_roll_number = models.CharField(max_length=15)
    isbn = models.BigIntegerField()
    issued_date = models.DateField(auto_now=True)
    expiry_date = models.DateField(default=expiry)