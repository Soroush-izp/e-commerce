from django.urls import path
from .views import (
    ProvinceWithCitiesView,
    AddressListCreateView,
    AddressDetailView,
    AdminAddressListCreateView,
    AdminAddressDetailView,
)

urlpatterns = [
    path(
        "api/provinces-with-cities/",
        ProvinceWithCitiesView.as_view(),
        name="provinces-with-cities",
    ),  # Get provinces with their cities
    path(
        "addresses/", AddressListCreateView.as_view(), name="address-list-create"
    ),  # GET (list) and POST (create)
    path(
        "addresses/<int:pk>/", AddressDetailView.as_view(), name="address-detail"
    ),  # GET, PUT, PATCH, DELETE by address ID
    path(
        "admin/addresses/",
        AdminAddressListCreateView.as_view(),
        name="admin-address-list-create",
    ),  # GET /?user_id=<user_id> user addresses / all addresses | Post send user in request body
    path(
        "admin/addresses/<int:pk>/",
        AdminAddressDetailView.as_view(),
        name="admin-address-detail",
    ),  # GET Retrieve address by id | PUT/PATCH Update specified address by id | DELETE specified address
]
