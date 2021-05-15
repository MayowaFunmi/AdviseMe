from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('list_users/', views.ListUserView.as_view(), name='list_user'),
    path('create_student_profile/', views.StudentProfileView.as_view(), name='create_student_profile'),
    path('create_councillor_profile/', views.CouncillorProfileView.as_view(), name='create_councillor_profile'),
    path('list_student_profile/<int:pk>/', views.ListStudentProfileView.as_view(), name='list_student_profile'),
    path('list_councillor_profile/<int:pk>/', views.ListCouncillorProfileView.as_view(), name='list_councillor_profile'),
    path('update_user/<int:pk>/', views.UpdateUserView.as_view(), name='update_user'),
    path('update_student_profile/<int:pk>/', views.UpdateStudentProfileView.as_view(), name='update_student_profile'),
    path('update_councillor_profile/<int:pk>/', views.UpdateCouncillorProfileView.as_view(), name='update_councillor_profile'),
    path('change_password/<int:pk>/', views.ChangePasswordView.as_view(), name='change_password'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('create_course/', views.CourseView.as_view(), name='create_course'),
    path('all_course_list/', views.AllCourseListView.as_view(), name='all_course_list'),
    path('register_course/', views.CourseRegistrationView.as_view(), name='register_course'),
    path('list_course_registration/', views.ListCourseRegistrationView.as_view(), name='list_course_registration'),
    path('create_student/', views.StudentView.as_view(), name='create_student'),
    path('list_all_student/', views.AllStudentListView.as_view(), name='list_all_student'),
]