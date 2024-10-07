from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .serializers import ProvinceWithCitiesSerializer, AddressSerializer
from .models import Address
from accounts.models import User
from iranian_cities.models import Ostan, Shahrestan
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from accounts.manager import IsSuperUser, IsRegularUser
# IsAdminUser => isStaff

class ProvinceWithCitiesView(ListAPIView):
    queryset = Ostan.objects.all()
    serializer_class = ProvinceWithCitiesSerializer


class AddressListCreateView(ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only addresses that belong to the authenticated user
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the authenticated user to the user field
        serializer.save(user=self.request.user)


class AddressDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return addresses that belong to the authenticated user
        return Address.objects.filter(user=self.request.user)


class AdminAddressListCreateView(ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]

    def get_queryset(self):
        # Get the user_id from the query parameters
        user_id = self.request.query_params.get("user_id", None)

        if user_id:
            # Return addresses for the specified user
            try:
                user = User.objects.get(id=user_id)
                return Address.objects.filter(user=user)
            except User.DoesNotExist:
                raise serializers.ValidationError({"user_id": "User not found."})
        else:
            # Return all addresses if no user_id is provided
            return Address.objects.all()


class AdminAddressDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]
    queryset = Address.objects.all()

    def get_queryset(self):
        # Admin/Superuser: return all addresses, allow access to specific address by ID
        return Address.objects.all()
