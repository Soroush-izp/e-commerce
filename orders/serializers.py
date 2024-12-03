from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import *
from catalog.models import Product, ProductSKU
from accounts.models import User
from accounts.serializers import UserSerializer
from locations.models import Address
from locations.serializers import AddressSerializer
from catalog.serializers import ProductSerializer, ProductSKUSerializer
from payments.models import PaymentDetails
from payments.serializers import PaymentDetailsSerializer

class WishlistDetailSerializer(serializers.ModelSerializer):
    product_info = ProductSerializer(source='product', read_only=True)  # Use nested serializer
    user_username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'product', 'user_username', 'product_info', 'created_at']


class ShopingCartSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    product_name = serializers.ReadOnlyField(source='product_sku.product.name')
    sku = serializers.ReadOnlyField(source='product_sku.sku')
    is_exist = serializers.BooleanField(read_only=True)

    class Meta:
        model = ShopingCart
        fields = [
            'id',
            'user',
            'product_sku',
            'sku',
            'product_name',
            'quantity',
            'price',
            'is_exist',
            'created_at',
            'updated_at',
        ]
        read_only_fields= ['price']

    def validate_quantity(self, value):
        """Ensure quantity does not exceed stock."""
        product_sku_id = self.initial_data.get('product_sku')
        try:
            product_sku = ProductSKU.objects.get(id=product_sku_id)
        except ProductSKU.DoesNotExist:
            raise serializers.ValidationError("Invalid product SKU.")

        if value > product_sku.quantity:
            raise serializers.ValidationError(
                f"Only {product_sku.quantity} units of {product_sku.sku} are available."
            )
        return value

    def validate(self, attrs):
        """Ensure product_sku is unique in the user's cart."""
        user = self.context['request'].user
        product_sku = attrs.get('product_sku')

        if ShopingCart.objects.filter(
            user=user, product_sku=product_sku
        ).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError(
                "This product with the selected SKU is already in your shopping cart."
            )
        return attrs

    def to_representation(self, instance):
        """Customize the output representation."""
        data = super().to_representation(instance)
        # Add any additional custom fields if necessary
        return data


# class PaymentDetailsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PaymentDetails
#         fields = ['id', 'amount', 'authority', 'status', 'ref_id', 'created_at', 'updated_at']
#         read_only_fields = fields  # Make all fields read-only


class OrderDetailSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField(read_only=True)  # Display related order items
    payment_info = PaymentDetailsSerializer(read_only=True)  # Include payment details

    class Meta:
        model = OrderDetails
        fields = ['id', 'user', 'address', 'total', 'status', 'created_at', 'updated_at', 'items', 'payment_info']
        read_only_fields = ['id', 'user', 'total', 'status', 'created_at', 'updated_at', 'items']

    def validate(self, attrs):
        """
        Ensure the user has items in their shopping cart.
        """
        user = self.context['request'].user
        if not ShopingCart.objects.filter(user=user).exists():
            raise serializers.ValidationError("Your shopping cart is empty.")
        return attrs

    def create(self, validated_data):
        """
        Create an order based on the user's shopping cart:
        - Validate stock availability
        - Transfer cart items to order items
        - Deduct stock and update order total
        - Clear the shopping cart after order creation
        """
        user = self.context['request'].user
        cart_items = ShopingCart.objects.filter(user=user)

        # Ensure all SKUs have enough stock
        insufficient_stock_items = [
            item for item in cart_items if item.quantity > item.product_sku.quantity
        ]
        if insufficient_stock_items:
            errors = [
                f"Insufficient stock for {item.product_sku.sku}. "
                f"Available: {item.product_sku.quantity}, Requested: {item.quantity}."
                for item in insufficient_stock_items
            ]
            raise serializers.ValidationError(errors)

        # Create the order
        order = OrderDetails.objects.create(user=user, address=validated_data['address'])

        # Create order items and update stock
        total = 0
        for cart_item in cart_items:
            product_sku = cart_item.product_sku
            total += cart_item.quantity * product_sku.price
            OrderItem.objects.create(
                order=order,
                product=product_sku.product,
                product_sku=product_sku,
                quantity=cart_item.quantity,
                price=product_sku.price,
            )
            # Deduct stock
            # product_sku.quantity -= cart_item.quantity
            product_sku.save()

        # Update order total and clear the cart
        order.total = total
        order.save()
        cart_items.delete()

        # Create PaymentDetails record
        PaymentDetails.objects.create(
            user=user,
            order=order,
            amount=total,  # Use the total amount from the order
            status='pending',  # Default status
        )

        return order
    
    def get_items(self, obj) -> list:
        """
        Retrieve order items associated with the order.
        """
        return UserOrderItemSerializer(obj.items.all(), many=True).data

    def to_representation(self, instance):
        """
        Ensure order item prices and total are accurate before returning.
        Check SKU existence and notify the user about invalid items.
        """
        # Safely check if payment exists
        payment = getattr(instance, 'payment', None)
    
        # Check SKU existence for each item
        invalid_items = []
        for item in instance.items.all():
            if not item.product_sku.is_active or item.product_sku.quantity <= 0:
                invalid_items.append(item)
    
        if invalid_items:
            # Collect errors for the user
            errors = [
                f"The product SKU '{item.product_sku.sku}' ({item.product.name}) is no longer available or out of stock."
                for item in invalid_items
            ]
    
            # Delete invalid items
            for item in invalid_items:
                item.delete()
    
            # Return error to the user
            raise serializers.ValidationError({"order_items": errors})
    
        # Update item prices if payment is pending or failed
        if not payment or payment.status in ['pending', 'failed']:
            for item in instance.items.all():
                if item.price != item.product_sku.price:
                    # Update the price of the order item if it has changed
                    item.price = item.product_sku.price
                    item.save()
    
            # Recalculate total
            instance.total = sum(item.price * item.quantity for item in instance.items.all())
            instance.save()
    
        # Proceed with default representation
        return super().to_representation(instance)


class AdminOrderDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Include full user details
    address = AddressSerializer(read_only=True)  # Include full address details
    items = serializers.SerializerMethodField()  # Related OrderItem details
    payment_info = PaymentDetailsSerializer(read_only=True)  # Include payment details

    class Meta:
        model = OrderDetails
        fields = ['id', 'user', 'address', 'total', 'status', 'created_at', 'updated_at', 'items', 'payment_info']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def to_representation(self, instance):
        """
        Ensure that:
        - Order items have up-to-date prices
        - Total order cost is recalculated if needed
        """
        payment = getattr(instance, 'payment', None)
        if not payment or payment.status in ['pending', 'failed']:
            for item in instance.items.all():
                if item.price != item.product_sku.price:
                    item.price = item.product_sku.price
                    item.save()

        # Recalculate total if payment is pending or missing
        if not payment or payment.status in ['pending', 'failed']:
            instance.total = sum(item.price * item.quantity for item in instance.items.all())
            instance.save()

        return super().to_representation(instance)
    
    def get_items(self, obj) -> list:
        """
        Retrieve serialized order items for this order.
        """
        return AdminOrderItemSerializer(obj.items.all(), many=True).data


class UserOrderDetailsSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)  # Include full address details
    items = serializers.SerializerMethodField()  # Related OrderItem details
    payment_info = PaymentDetailsSerializer(read_only=True)  # Include payment details

    class Meta:
        model = OrderDetails
        fields = ['id', 'address', 'total', 'status', 'created_at', 'updated_at', 'items', 'payment_info']
        read_only_fields = ['id', 'total', 'status', 'created_at', 'updated_at']

    def to_representation(self, instance):
        """
        Ensure order item prices and total are accurate before returning.
        """
        payment = getattr(instance, 'payment', None)
        if not payment or payment.status in ['pending', 'failed']:
            for item in instance.items.all():
                if item.price != item.product_sku.price:
                    item.price = item.product_sku.price
                    item.save()

        # Recalculate total if necessary
        if not payment or payment.status in ['pending', 'failed']:
            instance.total = sum(item.price * item.quantity for item in instance.items.all())
            instance.save()

        return super().to_representation(instance)

    def get_items(self, obj) -> list:
        """
        Retrieve serialized order items for this order.
        """
        return UserOrderItemSerializer(obj.items.all(), many=True).data


class AdminOrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Full product details
    product_sku = ProductSKUSerializer(read_only=True)  # Full SKU details
    total = serializers.SerializerMethodField()  # Calculated total field

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_sku', 'quantity', 'price', 'total', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_total(self, obj) -> int:
        """
        Calculate total as price * quantity.
        """
        return obj.price * obj.quantity


class UserOrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # Product name as a string
    product_sku = ProductSKUSerializer(read_only=True)  # SKU name as a string
    total = serializers.SerializerMethodField()  # Calculated total field

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_sku', 'quantity', 'price', 'total', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_total(self, obj) -> float:
        """
        Calculate total as price * quantity.
        """
        return obj.price * obj.quantity

