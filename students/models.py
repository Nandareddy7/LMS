from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    roll_number = models.CharField(max_length=15, unique=True)
    branch = models.CharField(max_length=30)
    mobile = models.BigIntegerField()
    email = models.CharField(max_length=50)
    profile = models.ImageField(upload_to="", null=True, blank=True) 