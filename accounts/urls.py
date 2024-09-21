# account/urls.py
from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserListView, GetUserView, UserProfileView

urlpatterns = [
   path("register/", UserRegistrationView.as_view(), name="register"),  # register
   path("login/", UserLoginView.as_view(), name="login"),   # login
   path("user-profile", UserProfileView.as_view(), name="user-profile"),   # profile edit
   path("users/", UserListView.as_view(), name="users-list"),  # list of users( staf mem)
   path("user/<int:id>", GetUserView.as_view(), name="user-details"),   # each user details edit( staf mem)
]
