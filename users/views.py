from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import StudentProfile
from .serializers import RegisterSerializer, ListUserSerializer, CreateStudentProfileSerializer, \
    ListStudentProfileSerializer, UpdateStudentProfileSerializer, UpdateUserSerializer, ChangePasswordSerializer, \
    LogoutSerializer

User = get_user_model()

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


#list individual student profiles
class ListStudentProfileView(generics.RetrieveAPIView):
    queryset = StudentProfile.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ListStudentProfileSerializer


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
