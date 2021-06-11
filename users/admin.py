from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentProfile, CouncillorProfile, CourseRegistration, Course, Student


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'status', 'email', 'registration_number', 'first_name', 'last_name']
    list_filter = ['registration_number']
    search_fields = ('status',)

# admin.site.register(CustomUser)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Course)
admin.site.register(CourseRegistration)
admin.site.register(StudentProfile)
admin.site.register(Student)
admin.site.register(CouncillorProfile)