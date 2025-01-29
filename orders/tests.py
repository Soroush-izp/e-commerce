from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import OrderDetails, ShopingCart, Wishlist
from accounts.models import User
from catalog.models import Product, ProductSKU
from locations.models import Address


class OrderTests(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username="testuser", password="testpass123", email="test@example.com"
        )
        self.client.force_authenticate(user=self.user)

        # Create test product
        self.product = Product.objects.create(name="Test Product", price=100)

        # Create test SKU
        self.sku = ProductSKU.objects.create(
            product=self.product, sku="TEST-SKU", quantity=10, price=100
        )

        # Create test address
        self.address = Address.objects.create(
            user=self.user, street="Test Street", city="Test City", postal_code="12345"
        )

    def test_add_to_cart(self):
        url = reverse("shopping-cart")
        data = {"product_sku": self.sku.id, "quantity": 2}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ShopingCart.objects.count(), 1)

    def test_create_order(self):
        # First add item to cart
        cart = ShopingCart.objects.create(
            user=self.user, product_sku=self.sku, quantity=1
        )

        url = reverse("user-order-list-create")
        data = {"address": self.address.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OrderDetails.objects.count(), 1)

    def test_add_to_wishlist(self):
        url = reverse("user-wishlist-list")
        data = {"product": self.product.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wishlist.objects.count(), 1)

    def test_order_status_update(self):
        """Test order status updates."""
        order = OrderDetails.objects.create(
            user=self.user, address=self.address, total=100
        )

        url = reverse("admin-order-detail", args=[order.id])
        data = {"status": "completed"}

        # Test with non-admin user
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Test with admin user
        admin_user = User.objects.create_superuser(
            "admin", "admin@test.com", "admin123"
        )
        self.client.force_authenticate(user=admin_user)
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(OrderDetails.objects.get(id=order.id).status, "completed")

    def test_cart_quantity_validation(self):
        """Test shopping cart quantity validation."""
        url = reverse("shopping-cart")
        data = {"product_sku": self.sku.id, "quantity": 0}  # Invalid quantity
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data["quantity"] = 101  # Exceeds maximum
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
