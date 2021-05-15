import re

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import StudentProfile, CouncillorProfile, Course, CourseRegistration, Student

# Register Serializer for user registration

User = get_user_model()


# register for all users
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'status', 'username', 'password', 'password2', 'registration_number', 'email', 'first_name', 'last_name')
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
            status=validated_data['status'],
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            registration_number=validated_data['registration_number'],
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


# create councillors profiles

class CreateCouncillorsProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouncillorProfile
        fields = ['title', 'user', 'qualification', 'discipline', 'birthday', 'years_of_exerience', 'gender', 'address',
                  'phone_number', 'country', 'profile_picture']

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
        councillor = CouncillorProfile.objects.create(
            title=validated_data['title'],
            user=validated_data['user'],
            qualification=validated_data['qualification'],
            discipline=validated_data['discipline'],
            years_of_exerience=validated_data['years_of_exerience'],
            birthday=validated_data['birthday'],
            gender=validated_data['gender'],
            address=validated_data['address'],
            phone_number=validated_data['phone_number'],
            country=validated_data['country'],
            profile_picture=validated_data['profile_picture'],
        )
        councillor.save()
        return councillor


# individual student profile list

class ListStudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = RegisterSerializer(instance.user).data
        return response


# individual councillor profile list

class ListCouncillorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouncillorProfile
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = RegisterSerializer(instance.user).data
        return response


# update user model data
class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        # extra_kwargs = {'first_name': {'required': True}, 'last_name': {'required': True}}

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({'email': "This email already exists"})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({'username': "This username already exists"})
        return value

    def update(self, instance, validated_data):
        # add checkpoint, logged in user only must be updated
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({'authorize': "You don't have permission to update this user"})
        #print(validated_data)
        instance.username = validated_data['username']
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']

        instance.save()
        return instance


# update student profile

class UpdateStudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['middle_name', 'student_level', 'birthday', 'gender', 'address', 'phone_number', 'country',
                  'profile_picture'
                  ]

    def update(self, instance, validated_data):
        # add checkpoint, logged in user only must be updated
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({'authorize': "You don't have permission to update this users details"})

        instance.middle_name = validated_data['middle_name']
        instance.student_level = validated_data['student_level']
        instance.birthday = validated_data['birthday']
        instance.gender = validated_data['gender']
        instance.address = validated_data['address']
        instance.phone_number = validated_data['phone_number']
        instance.country = validated_data['country']
        instance.profile_picture = validated_data['profile_picture']

        instance.save()
        return instance


# update councillor profile

class UpdateCouncillorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['title', 'qualification', 'discipline', 'birthday', 'years_of_exerience', 'gender', 'address',
                  'phone_number', 'country', 'profile_picture']

    def update(self, instance, validated_data):
        # add checkpoint, logged in user only must be updated
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({'authorize': "You don't have permission to update this users details"})

        instance.title = validated_data['title']
        instance.qualification = validated_data['qualification']
        instance.discipline = validated_data['discipline']
        instance.years_of_exerience = validated_data['years_of_exerience']
        instance.birthday = validated_data['birthday']
        instance.gender = validated_data['gender']
        instance.address = validated_data['address']
        instance.phone_number = validated_data['phone_number']
        instance.country = validated_data['country']
        instance.profile_picture = validated_data['profile_picture']
        instance.save()
        return instance


# change password

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': "Password fields didn't match"})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({'old_password': "old Password is not correct"})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({'authorize': "You don't have permission to change this user's password"})

        instance.set_password(validated_data['password'])
        instance.save()
        return instance


# logout serializer
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)
    #tokens = serializers.CharField(max_length=100, min_length=6, read_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        filtered_user_by_email = User.objects.filter(email=email)
        user = auth.authenticate(email=email, password=password)

        #if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
            #raise AuthenticationFailed(
                #detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }

        return super().validate(attrs)


# add course serializer
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('semester', 'course_code', 'course_name', 'course_type', 'course_unit', 'minimum_credit', 'maximum_credit')

    def create(self, validated_data):
        course = Course.objects.create(
            semester=validated_data['semester'],
            course_code=validated_data['course_code'],
            course_name=validated_data['course_name'],
            course_type=validated_data['course_type'],
            course_unit=validated_data['course_unit'],
            minimum_credit=validated_data['minimum_credit'],
            maximum_credit=validated_data['maximum_credit'],
        )
        course.save()
        return course


# list all courses
class AllCoursesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


# students create course registration

class CourseRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRegistration
        fields = ['name', 'courses_offered']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['name'] = RegisterSerializer(instance.name).data
        response['courses_offered'] = CourseSerializer(instance.courses_offered).data
        return response

    def create(self, validated_data):
        registration = CourseRegistration.objects.create(
            name=validated_data['name'],
            courses_offered=validated_data['courses_offered']
        )
        registration.save()
        return registration


# list all course registrations
class AllCoursesRegistrationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRegistration
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['name'] = RegisterSerializer(instance.name).data
        response['courses_offered'] = CourseSerializer(instance.courses_offered).data
        return response


# student data serializer for student model

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['name', 'profile', 'department', 'student_type', 'course_of_study', 'course_details']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['name'] = RegisterSerializer(instance.name).data
        response['profile'] = CreateStudentProfileSerializer(instance.profile).data
        response['course_details'] = CourseRegistrationSerializer(instance.course_details).data
        return response

    def create(self, validated_data):
        student = Student.objects.create(
            name=validated_data['name'],
            profile=validated_data['profile'],
            department=validated_data['department'],
            student_type=validated_data['student_type'],
            course_of_study=validated_data['course_of_study'],
            course_details=validated_data['course_details'],
        )
        student.save()
        return student


# list all students
class AllStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['name'] = RegisterSerializer(instance.name).data
        response['profile'] = CreateStudentProfileSerializer(instance.profile).data
        response['course_details'] = CourseRegistrationSerializer(instance.course_details).data
        return response
