from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import StudentProfile
from .serializers import RegisterSerializer, ListUserSerializer, CreateStudentProfileSerializer, \
    ListStudentProfileSerializer

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
    #permission_classes = (IsAuthenticated,)
    serializer_class = CreateStudentProfileSerializer


#list individual student profiles
class ListStudentProfileView(generics.RetrieveAPIView):
    queryset = StudentProfile.objects.all()
    #permission_classes = (IsAuthenticated,)
    serializer_class = ListStudentProfileSerializer
