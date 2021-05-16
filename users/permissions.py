from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission


User = get_user_model()


# custom permission for admins

class IsOnlyAdmin(BasePermission):
    def has_permission(self, request, view):
        user = User.objects.get(username=request.user)
        if user.is_superuser:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
