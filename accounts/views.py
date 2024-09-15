# account/views.py
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from .manager import IsSuperUser, IsRegularUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    UserSerializer,
)
from django.contrib.auth import get_user_model
from .models import User

class UserRegistrationView(CreateAPIView):
    # Handel user registration
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserLoginView(TokenObtainPairView):
    # Handle User Login and Provide jwt Tokens
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


class UserListView(ListAPIView):
    # Handle User List for saler
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdminUser, IsSuperUser]
