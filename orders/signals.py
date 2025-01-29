from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import OrderDetails, OrderItem, ShopingCart


@receiver(post_save, sender=OrderDetails)
def handle_order_status_change(sender, instance, created, **kwargs):
    """Handle order status changes."""
    if not created and instance.status == "completed":
        # Send notification to user
        # Update inventory
        pass


@receiver(post_save, sender=OrderItem)
def update_order_total(sender, instance, created, **kwargs):
    """Update order total when items change."""
    order = instance.order
    order.total = sum(item.price * item.quantity for item in order.items.all())
    order.save()


@receiver(pre_save, sender=ShopingCart)
def validate_stock(sender, instance, **kwargs):
    """Validate stock availability before saving cart item."""
    if instance.quantity > instance.product_sku.quantity:
        raise ValidationError(f"Only {instance.product_sku.quantity} units available")
