# account/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError, AuthenticationFailed

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
   password = serializers.CharField(write_only=True)

   class Meta:
      model = User
      fields = [
         "username",
         "email",
         "phone_number",
         "first_name",
         "last_name",
         "password",
      ]

   def validate(self, data):
      # Ensure that either email or phone_number is provided
      if not data.get("email") and not data.get("phone_number"):
         raise ValidationError("Either email or phone number is required.")

      # Validate password length
      if len(data.get("password", "")) < 8:
         raise ValidationError("Password must be at least 8 characters long.")

      return data

   def create(self, validated_data):
      user = User.objects.create_user(
         username=validated_data["username"],
         email=validated_data.get("email"),
         phone_number=validated_data.get("phone_number"),
         first_name=validated_data.get("first_name", ""),
         last_name=validated_data.get("last_name", ""),
         password=validated_data["password"],
      )
      return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
   def validate(self, attrs):
      data = super().validate(attrs)
      data["username"] = self.user.username
      data["email"] = self.user.email
      data["phone_number"] = self.user.phone_number
      return data


class UserLoginSerializer(serializers.Serializer):
   username = serializers.CharField(max_length=255)
   password = serializers.CharField(max_length=255, write_only=True)

   def validate(self, data):
      username = data.get("username")
      password = data.get("password")

      if not username or not password:
         raise ValidationError("Both username and password are required.")

      user = authenticate(username=username, password=password)
      if not user:
         raise AuthenticationFailed("Invalid username or password.")

      refresh = RefreshToken.for_user(user)
      return {
         "refresh": str(refresh),
         "access": str(refresh.access_token),
      }
      
      
class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = '__all__'
      extra_kwargs = {'password': {'write_only': True}}
