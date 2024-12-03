from django.db import models

class Wishlist(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(auto_now_add=True)


class ShopingCart(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='shopping_cart')
    product_sku = models.ForeignKey('catalog.ProductSKU', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'product_sku')  # Ensures uniqueness per user and SKU

    def __str__(self):
        return f"{self.user.username}: {self.product_sku.product.name} ({self.product_sku.sku}) - {self.quantity}"

    @property
    def is_exist(self):
        """Check if SKU is still active and has stock available."""
        return self.product_sku.is_active and self.product_sku.quantity > 0

    def save(self, *args, **kwargs):
        # Check SKU availability
        if self.quantity > self.product_sku.quantity:
            raise ValidationError(f"Only {self.product_sku.quantity} units of {self.product_sku.sku} are available.")

        # Update price dynamically
        self.price = self.quantity * self.product_sku.price

        # Ensure unique cart item
        if ShopingCart.objects.filter(user=self.user, product_sku=self.product_sku).exclude(pk=self.pk).exists():
            raise ValidationError("This product with the selected SKU is already in your shopping cart.")

        super().save(*args, **kwargs)


class OrderDetails(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', ('Pending')),
        ('completed', ('Completed')),
        ('shipped', ('Shipped')),
        ('canceled', ('Canceled')),
    ]

    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey('locations.Address', on_delete=models.CASCADE)
    total = models.IntegerField(default=0) 
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(OrderDetails, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE)
    product_sku = models.ForeignKey('catalog.ProductSKU', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.IntegerField(default=0) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Item {self.product.name} in Order #{self.order.id}"
