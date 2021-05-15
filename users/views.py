from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.response import Response
from .models import StudentProfile, CouncillorProfile, Course, CourseRegistration, Student
from .serializers import RegisterSerializer, ListUserSerializer, CreateStudentProfileSerializer, \
    ListStudentProfileSerializer, UpdateStudentProfileSerializer, UpdateUserSerializer, ChangePasswordSerializer, \
    LogoutSerializer, CreateCouncillorsProfileSerializer, ListCouncillorProfileSerializer, \
    UpdateCouncillorProfileSerializer, LoginSerializer, CourseSerializer, AllCoursesListSerializer, \
    CourseRegistrationSerializer, AllCoursesRegistrationListSerializer, StudentSerializer, AllStudentSerializer

User = get_user_model()


# custom permission for admins

class IsOnlyAdmin(BasePermission):
    def has_permission(self, request, view):
        user = User.objects.get(username=request.user)
        if request.user != user.is_superuser:
            pass


# user registration view


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


# user list view
class ListUserView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ListUserSerializer


# create student profile
class StudentProfileView(generics.CreateAPIView):
    queryset = StudentProfile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateStudentProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# create councillor profile
class CouncillorProfileView(generics.CreateAPIView):
    queryset = CouncillorProfile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateCouncillorsProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


#list individual student profiles
class ListStudentProfileView(generics.RetrieveAPIView):
    queryset = StudentProfile.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ListStudentProfileSerializer


#list individual councillor profiles
class ListCouncillorProfileView(generics.RetrieveAPIView):
    queryset = CouncillorProfile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ListCouncillorProfileSerializer


# update user
class UpdateUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer


#update student profiles
class UpdateStudentProfileView(generics.UpdateAPIView):
    queryset = StudentProfile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateStudentProfileSerializer


#update councillor profiles
class UpdateCouncillorProfileView(generics.UpdateAPIView):
    queryset = CouncillorProfile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateCouncillorProfileSerializer


# change password view
class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


# logout views
class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# create course view
class CourseView(generics.CreateAPIView):
    queryset = Course.objects.all()
    permission_classes = (IsOnlyAdmin,)    # add custom permission, only for admins
    serializer_class = CourseSerializer


# all courses list view
class AllCourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AllCoursesListSerializer


# create course registration view
class CourseRegistrationView(generics.CreateAPIView):
    queryset = CourseRegistration.objects.all()
    permission_classes = (AllowAny,)    # add custom permission, only for admins
    serializer_class = CourseRegistrationSerializer


# all courses list view
class ListCourseRegistrationView(generics.ListAPIView):
    queryset = CourseRegistration.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AllCoursesRegistrationListSerializer


# create student view
class StudentView(generics.CreateAPIView):
    queryset = Student.objects.all()
    permission_classes = (AllowAny,)    # add custom permission, only for admins
    serializer_class = StudentSerializer


# all student view
class AllStudentListView(generics.ListAPIView):
    queryset = Student.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = AllStudentSerializer
