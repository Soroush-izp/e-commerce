# account/views.py
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .manager import IsSuperUser, IsRegularUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import (
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    UserSerializer,
    UserProfileSerializer,
)
from django.contrib.auth import get_user_model
from .models import User


class UserRegistrationView(CreateAPIView):
    # Handel user registration
    serializer_class = UserRegistrationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)


class UserLoginView(TokenObtainPairView):
    # Handle User Login and Provide jwt Tokens
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


class UserListView(ListAPIView):
    # Handle User List for saler
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser, IsSuperUser]
    parser_classes = (MultiPartParser, FormParser)


class GetUserView(RetrieveUpdateDestroyAPIView):
    # Handle Each User ( by id )
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "id"
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser, IsSuperUser]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, id):
        try:
            user = self.get_object()
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserProfileView(RetrieveUpdateDestroyAPIView):
    # Handle profile for user
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        return self.request.user
