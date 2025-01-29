from django.contrib import admin
from .models import OrderDetails, OrderItem, Wishlist, ShopingCart


# Register models with admin site
@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "total", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["user__username", "id"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ["order", "product", "quantity", "price"]
    search_fields = ["order__id", "product__name"]


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "created_at"]
    search_fields = ["user__username", "product__name"]


@admin.register(ShopingCart)
class ShopingCartAdmin(admin.ModelAdmin):
    list_display = ["user", "product_sku", "quantity", "price", "created_at"]
    search_fields = ["user__username", "product_sku__sku"]
