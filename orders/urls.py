from django.urls import path
from .views import *

urlpatterns = [
    # Wishlist APIs for authenticated users
    # User: List all wishlists of the authenticated user (GET)
    path('wishlists/', AuthenticatedUserWishlistListView.as_view(), name='user-wishlist-list'),

    # User: Retrieve (GET), update (PUT, PATCH), or delete (DELETE) a specific wishlist item by ID
    path('wishlists/<int:pk>/', AuthenticatedUserWishlistDetailView.as_view(), name='user-wishlist-detail'),

    # Wishlist APIs for admin or superuser
    # Admin: Retrieve a list of all wishlists (GET)
    path('admin/wishlists/', AdminWishlistListView.as_view(), name='admin-wishlist-list'),

    # Admin: Retrieve (GET), update (PUT, PATCH), or delete (DELETE) a specific wishlist by ID
    path('admin/wishlists/<int:pk>/', AdminWishlistDetailView.as_view(), name='admin-wishlist-detail'),

    # Shopping Cart APIs for authenticated users
    # User: List all items in the authenticated user's shopping cart (GET) or add a new item (POST)
    path('shopping-cart/', ShopingCartListCreateView.as_view(), name='shopping-cart'),

    # User: Retrieve (GET), update (PUT, PATCH), or delete (DELETE) a specific shopping cart item by ID
    path('shopping-cart/<int:pk>/', ShopingCartDetailView.as_view(), name='shopping-cart-detail'),

    # Order APIs for admin or superuser
    # Admin: Retrieve a list of all orders (GET)
    path('admin/orders/', AdminOrderListView.as_view(), name='admin-order-list'),

    # Admin: Retrieve (GET), update (PUT, PATCH), or delete (DELETE) a specific order by ID
    path('admin/orders/<int:pk>/', AdminOrderDetailView.as_view(), name='admin-order-detail'),

    # Admin: Retrieve (GET), update (PUT, PATCH), or delete (DELETE) a specific order item by ID
    path('admin/order-items/<int:pk>/', AdminOrderItemDetailView.as_view(), name='admin-order-item-detail'),

    # Order APIs for authenticated users
    # User: List all orders of the authenticated user (GET) or create a new order (POST)
    path('user/orders/', UserOrderListCreateView.as_view(), name='user-order-list-create'),

    # User: Retrieve (GET), update (PUT, PATCH), or delete (DELETE) a specific order by ID
    path('user/orders/<int:pk>/', UserOrderDetailView.as_view(), name='user-order-detail'),

    # User: List all items for a specific order of the authenticated user (GET)
    path('user/orders/<int:order_id>/items/', UserOrderItemListView.as_view(), name='user-order-item-list'),
]
