from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .manager import CustomUserManager

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
   avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, default='avatars/default-avatar.jpg')
   email = models.EmailField(unique=True, blank=True, null=True)
   phone_number = models.CharField(max_length=15, unique=True, blank=True, null=True)
   username = models.CharField(max_length=255, unique=True)
   first_name = models.CharField(max_length=30, blank=True)
   last_name = models.CharField(max_length=30, blank=True)
   last_login = models.DateTimeField('Last Login', auto_now=True)
   birth_of_date = models.DateField(null=True, blank=True)
   created_at = models.DateTimeField('Created At', auto_now_add=True)
   is_active = models.BooleanField(default=True)
   is_staff = models.BooleanField(default=False)
   is_superuser = models.BooleanField(default=False)
   
   objects = CustomUserManager()

   USERNAME_FIELD = 'username'
   REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name']

   def __str__(self):
      return f'Username: {self.username} - Name: {self.first_name} {self.last_name}'
   
   @property
   def is_admin(self):
      return self.is_staff or self.is_superuser