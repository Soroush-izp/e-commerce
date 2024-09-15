from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models import Q
import re
from rest_framework.permissions import BasePermission


# for manage user permissions
class IsRegularUser(BasePermission):
    """
    Custom permission to only allow non-staff and non-superuser users(regular users).
    """

    def has_permission(self, request, view):
        # The user must be authenticated and not be staff or superuser (just regular user)
        return (
            request.user.is_authenticated
            and not request.user.is_staff
            and not request.user.is_superuser
        )


class IsSuperUser(BasePermission):
    """
    Custom permission to only allow superusers(have full access).
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


# for create costume user
class CustomUserManager(BaseUserManager):

    def create_user(self, username, password=None, **extra_fields):
        """
        Create and return a user with an email, phone number, or username.
        """
        if not username:
            raise ValueError("The Username field must be set")

        # Create the user instance
        user = self.model(username=username)
        user.set_password(password)  # Set the user's password
        user.save(using=self._db)  # Save the user to the database
        return user

    def create_superuser(self, username, password, phone_number, first_name, last_name):
        user = self.model(
            username=username,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
        )
        user.set_password(password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user
