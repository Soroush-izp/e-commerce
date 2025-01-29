from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import TimestampedModel, SoftDeleteModel


class Wishlist(TimestampedModel):
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="wishlist"
    )
    product = models.ForeignKey(
        "catalog.Product", on_delete=models.CASCADE, related_name="wishlisted_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)


class ShopingCart(TimestampedModel, SoftDeleteModel):
    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="shopping_cart"
    )
    product_sku = models.ForeignKey("catalog.ProductSKU", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.IntegerField(default=0)

    class Meta:
        unique_together = ("user", "product_sku")  # Ensures uniqueness per user and SKU

    def __str__(self):
        return f"{self.user.username}: {self.product_sku.product.name} ({self.product_sku.sku}) - {self.quantity}"

    @property
    def is_exist(self):
        """Check if SKU is still active and has stock available."""
        return self.product_sku.is_active and self.product_sku.quantity > 0

    def save(self, *args, **kwargs):
        # Check SKU availability
        if self.quantity > self.product_sku.quantity:
            raise ValidationError(
                f"Only {self.product_sku.quantity} units of {self.product_sku.sku} are available."
            )

        # Update price dynamically
        self.price = self.quantity * self.product_sku.price

        # Ensure unique cart item
        if (
            ShopingCart.objects.filter(user=self.user, product_sku=self.product_sku)
            .exclude(pk=self.pk)
            .exists()
        ):
            raise ValidationError(
                "This product with the selected SKU is already in your shopping cart."
            )

        super().save(*args, **kwargs)


class OrderDetails(TimestampedModel):
    """
    Represents an order in the system.
    
    Status choices:
    - pending: Order is created but not processed
    - completed: Order is successfully completed
    - shipped: Order has been shipped
    - canceled: Order was canceled
    """
    ORDER_STATUS_CHOICES = [
        ("pending", ("Pending")),
        ("completed", ("Completed")),
        ("shipped", ("Shipped")),
        ("canceled", ("Canceled")),
    ]

    user = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="orders"
    )
    address = models.ForeignKey("locations.Address", on_delete=models.CASCADE)
    total = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20, choices=ORDER_STATUS_CHOICES, default="pending"
    )

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

    class Meta:
        indexes = [
            models.Index(fields=["user", "status"]),
        ]


class OrderItem(TimestampedModel):
    order = models.ForeignKey(
        OrderDetails, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey("catalog.Product", on_delete=models.CASCADE)
    product_sku = models.ForeignKey("catalog.ProductSKU", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    price = models.IntegerField(default=0)

    def __str__(self):
        return f"Item {self.product.name} in Order #{self.order.id}"

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gt=0), name="positive_quantity"
            ),
            models.CheckConstraint(
                check=models.Q(price__gte=0), name="non_negative_price"
            ),
        ]
