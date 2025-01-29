# tests.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from accounts.models import User


class AccountAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a regular user
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            phone_number="1234567890",
            first_name="Test",
            last_name="User",
            password="TestPassword123!",
        )

        # Create an admin user
        self.admin_user = User.objects.create_superuser(
            username="adminuser",
            phone_number="0987654321",
            first_name="Admin",
            last_name="User",
            password="AdminPassword123!",
        )

        # URLs
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.user_profile_url = reverse("user-profile")
        self.users_list_url = reverse("users-list")
        self.user_detail_url = lambda id: reverse("user-details", args=[id])

    # Test user registration
    def test_user_registration(self):
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "phone_number": "1122334455",
            "first_name": "New",
            "last_name": "User",
            "password": "NewUserPassword123!",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    # Test user login
    def test_user_login(self):
        data = {"username": "testuser", "password": "TestPassword123!"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    # Test user profile retrieve
    def test_user_profile_retrieve(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.user_profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")

    # Test user profile update
    def test_user_profile_update(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "first_name": "Updated",
            "last_name": "User",
        }
        response = self.client.patch(self.user_profile_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")

    # Test retrieve users list ( admin only)
    def test_user_list_retrieval_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.users_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    # Test not retrieve users list ( non-admin only)
    def test_user_list_retrieval_non_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.users_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test retrieve user details by id ( admin only)
    def test_user_detail_retrieval_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.user_detail_url(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")

    # Test update user details by id ( admin only)
    def test_user_detail_update_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "first_name": "AdminUpdated",
        }
        response = self.client.patch(
            self.user_detail_url(self.user.id), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "AdminUpdated")

    # Test delete user by id ( admin only)
    def test_user_detail_deletion_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.user_detail_url(self.user.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    # Test delete user by id ( non-admin only)
    def test_user_detail_access_non_admin(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.user_detail_url(self.admin_user.id))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # test unauthenticated user can retrieve profile
    def test_user_profile_retrieval_unauthenticated(self):
        response = self.client.get(self.user_profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
