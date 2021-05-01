from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, StudentProfile, CouncillorProfile


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'registration_number', 'first_name', 'last_name']
    list_filter = ['username']
    #search_fields = ('registration_number',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(StudentProfile)
admin.site.register(CouncillorProfile)