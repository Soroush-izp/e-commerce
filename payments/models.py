from django.db import models


class PaymentDetails(models.Model):
    """
    Represents payment information for an order.
    
    Status choices:
    - pending: Payment is initiated but not completed
    - successful: Payment was successful
    - failed: Payment failed
    """
    PAYMENT_STATUS_CHOICES = [
        ("pending", ("Pending")),
        ("successful", ("Successful")),
        ("failed", ("Failed")),
    ]

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    order = models.OneToOneField(
        "orders.OrderDetails",
        on_delete=models.CASCADE,
        related_name="payment",
        null=True,
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount in Tomans
    authority = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default="pending"
    )
    ref_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.status}"
