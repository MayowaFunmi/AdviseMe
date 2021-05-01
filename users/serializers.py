import re

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import StudentProfile

# Register Serializer for user registration

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2', 'registration_number', 'email', 'first_name', 'last_name')
        # extra_kwargs = {'first_name': {'write_only': True}, 'last_name': {'write_only': True}

    def validate(self, attrs):
        username = attrs.get('username', '')
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': "Password fields didn't match"})

        if not username.isalnum():
            raise serializers.ValidationError('The username should only contain alphanumeric characters')

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            registration_number = validated_data['registration_number'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# list all registered users
class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        # extra_kwargs = {'password': {'write_only': True, 'required': True}} # this hides password from being seen

    def create(self, validated_data):   # this creates harshed password
        user = User.objects.create_user(**validated_data)
        return user


# create student profiles

class CreateStudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['user', 'middle_name', 'student_level', 'birthday', 'gender', 'address', 'phone_number', 'country',
                  'profile_picture'
                  ]

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = RegisterSerializer(instance.user).data
        return response

    def validate(self, attrs):
        phone_number = attrs.get('phone_number', '')
        if not re.match(r"(^[0]\d{10}$)|(^[\+]?[234]\d{12}$)", phone_number):
            raise serializers.ValidationError('This phone number is invalid')

        return attrs

    def create(self, validated_data):
        profile = StudentProfile.objects.create(
            user=validated_data['user'],
            middle_name=validated_data['middle_name'],
            student_level=validated_data['student_level'],
            birthday=validated_data['birthday'],
            gender=validated_data['gender'],
            address=validated_data['address'],
            phone_number=validated_data['phone_number'],
            country=validated_data['country'],
            profile_picture=validated_data['profile_picture'],
        )
        profile.save()
        return profile


# individual student profile serializer

class ListStudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = RegisterSerializer(instance.user).data
        return response
