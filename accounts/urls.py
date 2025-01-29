# account/urls.py
from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    UserListView,
    GetUserView,
    UserProfileView,
)

urlpatterns = [
    path(
        "register/", UserRegistrationView.as_view(), name="register"
    ),  # User: register
    path("login/", UserLoginView.as_view(), name="login"),  # AllUsers: login
    path(
        "user-profile", UserProfileView.as_view(), name="user-profile"
    ),  # AllUsers: profile edit
    path(
        "admin/users/", UserListView.as_view(), name="users-list"
    ),  # Staf: list of users
    path(
        "admin/user/<int:id>", GetUserView.as_view(), name="user-details"
    ),  # Staf: each user details edit
]
