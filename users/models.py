from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class CustomUser(AbstractUser):
    STATUS = [
        ('student', 'student'),
        ('Course Adviser', 'Course Adviser'),
    ]
    registration_number = models.CharField(max_length=100)
    status = models.CharField(choices=STATUS, default=STATUS[0], max_length=20)

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


User = get_user_model()


class Course(models.Model):
    SEMESTER = [
        ('First Semester', 'First Semester'),
        ('Second Semester', 'Second Semester'),
    ]
    COURSE_TYPE = [
        ('Core Course', 'Core Course'),
        ('Elective Course', 'Elective Course'),
    ]
    semester = models.CharField(choices=SEMESTER, default=SEMESTER[0], max_length=30)
    course_code = models.CharField(max_length=10)
    course_name = models.CharField(max_length=55)
    course_type = models.CharField(choices=COURSE_TYPE, default=COURSE_TYPE[0], max_length=30)
    course_unit = models.DecimalField(max_digits=2, decimal_places=1)
    minimum_credit = models.PositiveIntegerField(default=1)
    maximum_credit = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.course_name} ({self.course_code})'

    def total_course_units(self):
        return sum(course.each_course_unit() for course in self.courses.all())

    def total_min_credit(self):
        return sum(course.each_min_credit() for course in self.courses.all())

    def total_max_credit(self):
        return sum(course.each_max_credit() for course in self.courses.all())


class CourseRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses_offered = models.ForeignKey(Course, related_name='course_registration', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.courses_offered} offered by {self.name}'

    def each_course_unit(self):
        return self.courses_offered.course_unit

    def each_min_credit(self):
        return self.courses_offered.minimum_credit

    def each_max_credit(self):
        return self.courses_offered.maximum_credit


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


class Student(models.Model):
    STUDENT_TYPE = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
    ]
    DEPARTMENT = [
        ('Information and Media Studies', 'Information and Media Studies'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(StudentProfile, related_name='students', on_delete=models.CASCADE)
    department = models.CharField(choices=DEPARTMENT, default=DEPARTMENT[0], max_length=100)
    student_type = models.CharField(choices=STUDENT_TYPE, default=STUDENT_TYPE[0], max_length=20)
    course_of_study = models.CharField(max_length=100)
    course_details = models.ForeignKey(CourseRegistration, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


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
    years_of_experience = models.CharField(max_length=10, help_text='How many years of academic experience do you have?')
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