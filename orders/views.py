from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError, NotFound
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_field, OpenApiParameter
from .serializers import *
from accounts.manager import IsSuperUser  # custom permission
from core.utils import cache_response
from django.core.exceptions import ObjectDoesNotExist


@extend_schema(
    methods=["GET"],
    summary="List User's Wishlist",
    description="Retrieve the authenticated user's wishlist. Each user can only view their own wishlist.",
    tags=["Wishlist"],
)
@extend_schema(
    methods=["POST"],
    summary="Add Product to Wishlist",
    description="Add a new product to the authenticated user's wishlist.",
    request=WishlistDetailSerializer,
    tags=["Wishlist"],
)
class AuthenticatedUserWishlistListView(generics.ListCreateAPIView):
    """
    View for authenticated users to list and create their own wishlists.
    Only the owner can see or create their wishlists.
    """

    serializer_class = WishlistDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure only the user's own wishlist is visible
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the current user with the new wishlist
        serializer.save(user=self.request.user)


@extend_schema(
    methods=["GET"],
    summary="Retrieve Wishlist Item",
    description="Retrieve details of a specific product in the authenticated user's wishlist.",
    tags=["Wishlist"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Remove Product from Wishlist",
    description="Remove a specific product from the authenticated user's wishlist.",
    tags=["Wishlist"],
)
class AuthenticatedUserWishlistDetailView(generics.RetrieveDestroyAPIView):
    """
    View for authenticated users to retrieve or delete their specific wishlist.
    """

    serializer_class = WishlistDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Ensure only the user's own wishlist is accessible
        return Wishlist.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        # Optional: Ensure users can only delete their own wishlist
        wishlist = self.get_object()
        if wishlist.user != request.user:
            raise PermissionDenied(
                "You do not have permission to delete this wishlist."
            )
        return super().delete(request, *args, **kwargs)


@extend_schema(
    methods=["GET"],
    summary="List All Wishlists",
    description="Retrieve a list of all wishlists. Accessible only to admin or superuser.",
    tags=["Wishlist (Admin)"],
)
class AdminWishlistListView(generics.ListAPIView):
    """
    Admin view for listing all wishlists.
    Accessible only to admin or superuser.
    """

    queryset = Wishlist.objects.all()
    serializer_class = WishlistDetailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


@extend_schema(
    methods=["GET"],
    summary="Retrieve Any Wishlist Item",
    description="Retrieve details of any product in a user's wishlist. Accessible only to admin or superuser.",
    tags=["Wishlist (Admin)"],
)
@extend_schema(
    methods=["PUT", "PATCH"],
    summary="Update Wishlist Item",
    description="Update a specific wishlist item. Accessible only to admin or superuser.",
    request=WishlistDetailSerializer,
    tags=["Wishlist (Admin)"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Delete Wishlist Item",
    description="Remove a specific product from any user's wishlist. Accessible only to admin or superuser.",
    tags=["Wishlist (Admin)"],
)
class AdminWishlistDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Admin view for retrieving, updating, or deleting any user's wishlist.
    Accessible only to admin or superuser.
    """

    queryset = Wishlist.objects.all()
    serializer_class = WishlistDetailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


@extend_schema(
    methods=["GET"],
    summary="List User's Shopping Cart",
    description="Retrieve the current user's shopping cart items.",
    responses={
        200: ShopingCartSerializer(many=True),
        401: {"description": "Authentication credentials were not provided."},
    },
    tags=["Shopping Cart"],
)
class ShopingCartListCreateView(generics.ListCreateAPIView):
    """
    View for managing shopping cart items.

    list:
    Return a list of all items in the user's shopping cart.

    create:
    Add a new item to the shopping cart.
    """

    serializer_class = ShopingCartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            return ShopingCart.objects.filter(user=self.request.user)
        except Exception:
            raise NotFound(detail="No shopping cart found")

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except ValidationError as e:
            raise ValidationError(detail=str(e))
        except Exception as e:
            raise ValidationError(detail="Unable to add item to cart")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Calculate the total price for all shopping carts of the user
        total_price = sum(
            float(cart["price"]) * int(cart["quantity"]) for cart in serializer.data
        )

        # Customize the response
        return Response({"total_price": total_price, "carts": serializer.data})


@extend_schema(
    methods=["GET"],
    summary="Retrieve Shopping Cart Item",
    description="Retrieve details of a specific item in the authenticated user's shopping cart.",
    tags=["Shopping Cart"],
)
@extend_schema(
    methods=["PUT", "PATCH"],
    summary="Update Shopping Cart Item",
    description="Update the quantity of a specific product in the authenticated user's shopping cart.",
    request=ShopingCartSerializer,
    tags=["Shopping Cart"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Remove Item from Shopping Cart",
    description="Remove a specific product SKU from the authenticated user's shopping cart.",
    tags=["Shopping Cart"],
)
class ShopingCartDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a specific shopping cart item for the authenticated user.
    """

    serializer_class = ShopingCartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ShopingCart.objects.filter(user=self.request.user)


# Admin: List all orders
@extend_schema(
    methods=["GET"],
    summary="List All Orders",
    description="Retrieve a list of all orders with detailed information. Accessible to admin users only.",
    tags=["Orders (Admin)"],
)
class AdminOrderListView(generics.ListAPIView):
    """
    Admin Access:
    - GET: List all orders with detailed information.
    """

    serializer_class = AdminOrderDetailsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = OrderDetails.objects.all()


# Admin: Retrieve, update, and delete specific order
@extend_schema(
    methods=["GET"],
    summary="Retrieve Specific Order",
    description="Retrieve detailed information about a specific order. Accessible to admin users only.",
    tags=["Orders (Admin)"],
)
@extend_schema(
    methods=["PUT", "PATCH"],
    summary="Update Order Details",
    description="Update the details of a specific order, such as its status. Accessible to admin users only.",
    request=AdminOrderDetailsSerializer,
    tags=["Orders (Admin)"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Delete Order",
    description="Remove a specific order from the system. Accessible to admin users only.",
    tags=["Orders (Admin)"],
)
class AdminOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Admin Access:
    - GET: Retrieve details of a specific order.
    - PUT/PATCH: Update order details like status.
    - DELETE: Remove an order.
    """

    serializer_class = AdminOrderDetailsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = OrderDetails.objects.all()


# Admin: Retrieve, update, and delete specific order item
@extend_schema(
    methods=["GET"],
    summary="Retrieve Order Item Details",
    description="Retrieve detailed information about a specific order item. Accessible to admin users only.",
    tags=["Order Items (Admin)"],
)
@extend_schema(
    methods=["PUT", "PATCH"],
    summary="Update Order Item",
    description="Update details of a specific order item, such as quantity or price. Accessible to admin users only.",
    request=AdminOrderItemSerializer,
    tags=["Order Items (Admin)"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Delete Order Item",
    description="Remove a specific order item from an order. Accessible to admin users only.",
    tags=["Order Items (Admin)"],
)
class AdminOrderItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Admin Access:
    - GET: Retrieve details of a specific order item.
    - PUT/PATCH: Update order item details like quantity or price.
    - DELETE: Remove an order item from the order.
    """

    serializer_class = AdminOrderItemSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = OrderItem.objects.all()


# User: List and create orders
@extend_schema(
    methods=["GET"],
    summary="List User Orders",
    description="Retrieve a list of all orders placed by the authenticated user.",
    tags=["Orders (User)"],
)
@extend_schema(
    methods=["POST"],
    summary="Create New Order",
    description="Create a new order for the authenticated user based on their shopping cart.",
    request=OrderDetailSerializer,
    tags=["Orders (User)"],
)
class UserOrderListCreateView(generics.ListCreateAPIView):
    """
    User Access:
    - GET: List all orders for the authenticated user.
    - POST: Create a new order using the user's shopping cart.
    """

    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return orders belonging to the authenticated user.
        """
        return OrderDetails.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Create a new order for the authenticated user.
        """
        try:
            serializer.save(user=self.request.user)
        except ValidationError as e:
            raise ValidationError({"detail": str(e)})

    @cache_response(timeout=300)
    def list(self, request, *args, **kwargs):
        queryset = (
            self.get_queryset()
            .select_related("user", "address")
            .prefetch_related("items__product", "items__product_sku")
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# User: Retrieve specific order details
@extend_schema(
    methods=["GET"],
    summary="Retrieve User Order Details",
    description="Retrieve detailed information about a specific order placed by the authenticated user.",
    tags=["Orders (User)"],
)
class UserOrderDetailView(generics.RetrieveAPIView):
    """
    User Access:
    - GET: Retrieve detailed information about a specific order.
    """

    serializer_class = UserOrderDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Ensure the user can only retrieve their own orders.
        """
        return OrderDetails.objects.filter(user=self.request.user)


# User: List all items in a specific order
@extend_schema(
    methods=["GET"],
    summary="List Items in User Order",
    description="Retrieve a list of all items in a specific order placed by the authenticated user.",
    tags=["Order Items (User)"],
)
class UserOrderItemListView(generics.ListAPIView):
    """
    User Access:
    - GET: List all items in a specific order for the authenticated user.
    """

    serializer_class = UserOrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return order items for the authenticated user's specific order.
        """
        order_id = self.kwargs.get("order_id")
        return OrderItem.objects.filter(
            order__id=order_id, order__user=self.request.user
        )


class OrderDetailView(generics.RetrieveAPIView):
    """
    Retrieve a specific order.

    This endpoint allows authenticated users to retrieve details of their orders.
    Admin users can access any order in the system.

    Permissions:
    - User must be authenticated
    - Regular users can only access their own orders
    - Admin users can access any order

    Parameters:
    - pk (path): The ID of the order to retrieve

    Returns:
    - 200: Order details retrieved successfully
    - 404: Order not found
    - 403: User does not have permission to access this order
    """
