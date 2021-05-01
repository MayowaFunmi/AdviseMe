from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('list_users/', views.ListUserView.as_view(), name='list_user'),
    path('create_student_profile/', views.StudentProfileView.as_view(), name='create_student_profile'),
    path('list_student_profile/<int:pk>/', views.ListStudentProfileView.as_view(), name='list_student_profile'),
]