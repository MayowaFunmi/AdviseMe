from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    registration_number = models.CharField(max_length=100)


User = get_user_model()


# model for students' profile
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    middle_name = models.CharField(max_length=100, help_text='Enter your middle name here if any')
    course = models.CharField(max_length=100, help_text='Enter your course of study')
    student_level = models.CharField(max_length=100)
    birthday = models.DateField()
    GENDER = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(choices=GENDER, max_length=10)
    address = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=30)
    country = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pics/%Y/%m/%d/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


# model for councillors
class CouncillorProfile(models.Model):
    TITLE = [
        ('Prof', 'Prof'),
        ('Dr', 'Dr'),
        ('Engr', 'Engr'),
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs')
    ]
    title = models.CharField(choices=TITLE, default='Choose Your Title', max_length=10)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=100, help_text='What is your qualification?')
    discipline = models.CharField(max_length=100, help_text='What is your area/field of discipline?')
    years_of_exerience = models.CharField(max_length=10, help_text='How many years of academic experience do you have?')
    birthday = models.DateField()
    GENDER = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(choices=GENDER, max_length=10)
    address = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=30)
    country = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pics/%Y/%m/%d/', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}. {self.user.first_name} {self.user.last_name}'
