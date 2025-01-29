from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from django.db import transaction
from .models import *


# Brand serializers
class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        # Safely get the request object from the context
        request = kwargs.get("context", {}).get("request", None)
        super().__init__(*args, **kwargs)

        if request is not None:
            if request.method == "GET":
                # For GET requests, include only specific fields
                allowed_fields = [
                    "id",
                    "brand_name",
                    "icon",
                    "is_active",
                ]  # Define allowed fields
                self.fields = {field: self.fields[field] for field in allowed_fields}
            else:
                # For other methods, include all fields (default behavior)
                pass


class BrandPhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = BrandPhoto
        fields = "__all__"  # Use 'brand' for brand ID

    def validate_brand(self, value):
        # Check if the brand with this ID exists
        if not Brand.objects.filter(id=value).exists():
            raise serializers.ValidationError("Brand with this ID does not exist.")
        return value


class BrandVideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = BrandVideo
        fields = "__all__"  # Use 'brand' for brand ID

    def validate_brand(self, value):
        # Check if the brand with this ID exists
        try:
            Brand.objects.get(id=value.id)
        except Brand.DoesNotExist:
            raise serializers.ValidationError("Brand with this ID does not exist.")
        return value


class BrandDetailSerializer(serializers.ModelSerializer):
    photos = BrandPhotoSerializer(many=True, read_only=True)  # Nested photos
    videos = BrandVideoSerializer(many=True, read_only=True)  # Nested videos

    class Meta:
        model = Brand
        fields = [
            "id",
            "brand_name",
            "description",
            "website",
            "instagram",
            "facebook",
            "icon",
            "is_active",
            "photos",
            "videos",
        ]

    # Attribute serializers


class AttributeTypeSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)  # Make it read-only

    class Meta:
        model = AttributeType
        fields = ["id", "name", "created_at", "is_active"]


class AttributeGroupSerializer(serializers.ModelSerializer):
    # Use PrimaryKeyRelatedField for accepting a list of AttributeType IDs
    attributes = serializers.PrimaryKeyRelatedField(
        many=True, queryset=AttributeType.objects.all()
    )
    created_at = serializers.DateTimeField(read_only=True)  # Make it read-only

    # Read-only field to display full AttributeTypeSerializer data for selected attributes
    attribute_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AttributeGroup
        fields = [
            "id",
            "name",
            "attributes",
            "created_at",
            "is_active",
            "attribute_details",
        ]

    def get_attribute_details(self, obj) -> list[dict]:
        # Fetch the related AttributeType objects and serialize them
        attributes = obj.attributes.all()
        return AttributeTypeSerializer(attributes, many=True).data


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    # Change type to PrimaryKeyRelatedField to only return the ID
    type = serializers.PrimaryKeyRelatedField(queryset=AttributeType.objects.all())
    created_at = serializers.DateTimeField(read_only=True)  # Make it read-only

    # Add a new field that uses the AttributeTypeSerializer to return full details
    type_data = serializers.SerializerMethodField()

    class Meta:
        model = ProductAttributeValue
        fields = ["id", "type", "type_data", "value", "created_at", "is_active"]

    def get_type_data(self, obj) -> dict:
        # Return the serialized data for the AttributeType instance
        return AttributeTypeSerializer(obj.type).data


class AdminCategorySerializer(serializers.ModelSerializer):
    all_attribute_groups = AttributeGroupSerializer(
        many=True, read_only=True
    )  # For combined parent and category groups
    created_at = serializers.DateTimeField(read_only=True)  # Make it read-only
    level = serializers.IntegerField(read_only=True)  # Make level read-only

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "parent",
            "attribute_groups",
            "all_attribute_groups",
            "photo",
            "description",
            "level",
            "created_at",
            "is_active",
        ]

    def to_representation(self, instance):
        """Override to include parent attribute groups combined with the category's own."""
        representation = super().to_representation(instance)
        representation["all_attribute_groups"] = AttributeGroupSerializer(
            instance.get_all_attribute_groups(), many=True
        ).data
        return representation


# Serializer for listing categories for users
class UserCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "photo", "level", "is_active"]


# # Serializer for category detail view for users
class UserCategoryDetailSerializer(serializers.ModelSerializer):
    all_attribute_groups = AttributeGroupSerializer(many=True, read_only=True)
    subcategories = serializers.SerializerMethodField()
    parent_category = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "parent",
            "photo",
            "description",
            "level",
            "is_active",
            "all_attribute_groups",
            "subcategories",
            "parent_category",
        ]

    def get_subcategories(self, instance) -> list[dict]:
        """Get the subcategories of the current category."""
        # Retrieve only active subcategories
        subcategories = instance.subcategories.filter(is_active=True)
        return UserCategoryListSerializer(subcategories, many=True).data

    def get_parent_category(self, instance) -> list[dict]:
        """Get the parent category if it exists."""
        if instance.parent:
            return UserCategoryListSerializer(instance.parent).data
        return None


# Serializer for nested categories (parent-child)
class CategoryTreeSerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "subcategories"]

    def get_subcategories(self, instance) -> list[dict]:
        """Recursively get subcategories for the tree structure."""
        # Filter active subcategories
        active_subcategories = instance.subcategories.filter(is_active=True)
        # Serialize them using the same serializer (recursive approach)
        return CategoryTreeSerializer(active_subcategories, many=True).data


# Serializer for list all products
class ProductListSerializer(serializers.ModelSerializer):
    attribute_groups = serializers.SerializerMethodField()  # Get attribute groups
    price_range = serializers.SerializerMethodField()  # Get price range
    is_available = serializers.SerializerMethodField()  # Check if product is available

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "cover",
            "category",
            "attribute_groups",
            "price_range",
            "is_available",
            "created_at",
            "is_active",
        ]

    def get_attribute_groups(self, obj) -> list[dict]:
        return [
            {"id": group.id, "name": group.name}
            for group in obj.category.get_all_attribute_groups()
        ]

    def get_price_range(self, obj) -> dict:
        prices = obj.skus.values_list("price", flat=True)
        if prices:
            return {"min_price": min(prices), "max_price": max(prices)}
        return {"min_price": 0, "max_price": 0}

    def get_is_available(self, obj) -> bool:
        # Check if any SKU of the product has quantity > 0
        return obj.skus.filter(quantity__gt=0).exists()


class ProductSerializer(serializers.ModelSerializer):
    attribute_groups = serializers.SerializerMethodField()  # Get attribute groups
    price_range = serializers.SerializerMethodField()  # Get price range
    is_available = serializers.SerializerMethodField()  # Check if product is available

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "summary",
            "cover",
            "category",
            "attribute_groups",
            "price_range",
            "is_available",
            "created_at",
            "is_active",
        ]

    def get_attribute_groups(self, obj) -> list[dict]:
        return [
            {"id": group.id, "name": group.name}
            for group in obj.category.get_all_attribute_groups()
        ]

    def get_price_range(self, obj) -> dict:
        prices = obj.skus.values_list("price", flat=True)
        if prices:
            return {"min_price": min(prices), "max_price": max(prices)}
        return {"min_price": 0, "max_price": 0}

    def get_is_available(self, obj) -> bool:
        # Check if any SKU of the product has quantity > 0
        return obj.skus.filter(quantity__gt=0).exists()


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = ["id", "product", "title", "value", "order_num"]
        extra_kwargs = {"product": {"required": True}, "order_num": {"required": True}}

    def validate(self, data):
        product = data.get("product")
        order_num = data.get("order_num")
        if ProductDetail.objects.filter(product=product, order_num=order_num).exists():
            raise serializers.ValidationError(
                "Order number must be unique per product."
            )
        return data


class ProductDetailOrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDetail
        fields = ["id", "order_num", "product"]


class ProductDetailUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    order_num = serializers.IntegerField()


class ProductDetailBatchUpdateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    updates = ProductDetailUpdateSerializer(many=True)

    def update(self, instance, validated_data):
        product_id = validated_data.get("product_id")
        update_data = validated_data.get("updates", [])

        # Fetch existing ProductDetail instances for the specified product
        existing_details = ProductDetail.objects.filter(product_id=product_id)
        existing_ids = set(existing_details.values_list("id", flat=True))

        # Extract the IDs from the update data
        update_ids = {item["id"] for item in update_data}

        # Check if all the provided IDs in updates belong to the specified product
        if not update_ids.issubset(existing_ids):
            raise serializers.ValidationError(
                "Some ProductDetail IDs do not belong to the specified product."
            )

        with transaction.atomic():
            # Step 1: Delete any ProductDetail records that are not in the update list
            ProductDetail.objects.filter(product_id=product_id).exclude(
                id__in=update_ids
            ).delete()

            # Step 2: Update order_num for the remaining ProductDetail instances using temporary values
            # Assign temporary order values to avoid unique constraint issues
            temp_order_num = (
                max(
                    ProductDetail.objects.filter(product_id=product_id).values_list(
                        "order_num", flat=True
                    )
                )
                + 1
            )

            # Temporarily set all order numbers to a value outside the current range
            for update_item in update_data:
                detail_id = update_item["id"]
                temp_order_num += 1
                ProductDetail.objects.filter(id=detail_id).update(
                    order_num=temp_order_num
                )

            # Step 3: Set the final order_num values
            for update_item in update_data:
                detail_id = update_item["id"]
                order_num = update_item["order_num"]
                ProductDetail.objects.filter(id=detail_id).update(order_num=order_num)

        return instance


class ProductPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhoto
        fields = ["id", "product", "alt", "photo", "uploaded_at"]
        extra_kwargs = {"photo": {"required": True}, "alt": {"required": True}}


class ProductVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVideo
        fields = ["id", "product", "alt", "video", "uploaded_at"]
        extra_kwargs = {"video": {"required": True}, "alt": {"required": True}}

    def validate_video(self, value):
        mime_type, encoding = mimetypes.guess_type(value.name)
        if mime_type and not mime_type.startswith("video"):
            raise serializers.ValidationError("Uploaded file is not a valid video.")
        return value


class ProductSKUAttributeSerializer(serializers.ModelSerializer):
    # Use ProductAttributeValueSerializer to display attribute value details
    show_attribute_values = ProductAttributeValueSerializer(
        source="attribute_value", read_only=True
    )  # Use the existing attribute_value as source

    class Meta:
        model = ProductSKUAttribute
        fields = ["id", "sku", "attribute_value", "show_attribute_values"]
        read_only_fields = ["show_attribute_values"]


class ProductSKUSerializer(serializers.ModelSerializer):
    # Display a read-only list of related ProductSKUAttributeSerializer entries
    sku_attributes = ProductSKUAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = ProductSKU
        fields = [
            "id",
            "sku",
            "product",
            "price",
            "quantity",
            "sku_attributes",
            "created_at",
            "is_active",
        ]
        read_only_fields = ["sku", "created_at", "sku_attributes"]


#       Review serializers
# Serializer for ReviewSection model
class ReviewSectionSerializer(serializers.ModelSerializer):
    texts = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )  # Displays list of ReviewText IDs associated with this section
    photos = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )  # Displays list of ReviewPhoto IDs associated with this section
    videos = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )  # Displays list of ReviewVideo IDs associated with this section

    class Meta:
        model = ReviewSection
        fields = [
            "id",
            "product",
            "title",
            "order_num",
            "texts",
            "photos",
            "videos",
        ]  # Includes foreign key product, title, and related fields
        read_only_fields = [
            "order_num"
        ]  # Ensures order_num is read-only as it is auto-generated


# Serializer for ReviewText model
class ReviewTextSerializer(serializers.ModelSerializer):
    review_section = serializers.PrimaryKeyRelatedField(
        queryset=ReviewSection.objects.all()
    )  # Allows linking to a ReviewSection

    class Meta:
        model = ReviewText
        fields = [
            "id",
            "review_section",
            "text",
            "order_num",
        ]  # Includes foreign key review_section and review text
        read_only_fields = ["order_num"]  # Ensures order_num is read-only


# Serializer for ReviewPhoto model
class ReviewPhotoSerializer(serializers.ModelSerializer):
    review_section = serializers.PrimaryKeyRelatedField(
        queryset=ReviewSection.objects.all()
    )  # Allows linking to a ReviewSection
    position = serializers.ChoiceField(
        choices=ReviewPhoto.POSITION_CHOICES
    )  # Allows selection from predefined choices

    class Meta:
        model = ReviewPhoto
        fields = [
            "id",
            "review_section",
            "image",
            "position",
            "order_num",
        ]  # Includes foreign key review_section, image, position, and order number
        read_only_fields = ["order_num"]  # Ensures order_num is read-only


# Serializer for ReviewVideo model
class ReviewVideoSerializer(serializers.ModelSerializer):
    review_section = serializers.PrimaryKeyRelatedField(
        queryset=ReviewSection.objects.all()
    )  # Allows linking to a ReviewSection

    class Meta:
        model = ReviewVideo
        fields = [
            "id",
            "review_section",
            "video",
            "order_num",
        ]  # Includes foreign key review_section, video file, and order number
        read_only_fields = ["order_num"]  # Ensures order_num is read-only


# Nested serializer for including ReviewText, ReviewPhoto, and ReviewVideo details within ReviewSection
class ReviewSectionDetailSerializer(serializers.ModelSerializer):
    # Existing PrimaryKeyRelatedFields for ID-only references
    texts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    photos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    videos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # Combine texts, photos, and videos into a single ordered list
    items = serializers.SerializerMethodField()

    class Meta:
        model = ReviewSection
        fields = [
            "id",
            "product",
            "title",
            "order_num",
            "texts",
            "photos",
            "videos",  # ID-only references
            "items",
        ]
        # read_only_fields = ['order_num']

    def get_items(self, obj) -> list[dict]:
        # Retrieve all related texts, photos, and videos
        texts = obj.texts.all()
        photos = obj.photos.all()
        videos = obj.videos.all()

        # Serialize each related item
        texts_serialized = ReviewTextSerializer(texts, many=True).data
        photos_serialized = ReviewPhotoSerializer(photos, many=True).data
        videos_serialized = ReviewVideoSerializer(videos, many=True).data

        # Add an identifier to each serialized item type
        for item in texts_serialized:
            item["type"] = "text"
        for item in photos_serialized:
            item["type"] = "photo"
        for item in videos_serialized:
            item["type"] = "video"

        # Combine all serialized items into a single list
        combined_items = texts_serialized + photos_serialized + videos_serialized

        # Sort by 'order_num' and return the list
        return sorted(combined_items, key=lambda x: x["order_num"])


class SwapOrderNumSerializer(serializers.Serializer):
    id1 = serializers.IntegerField()  # ID of the first object
    id2 = serializers.IntegerField()  # ID of the second object

    def validate(self, data):
        # Ensure id1 and id2 are not the same
        if data["id1"] == data["id2"]:
            raise serializers.ValidationError(
                "The IDs must be different to swap order numbers."
            )
        return data


class SwapOrderNumItemsSerializer(serializers.Serializer):
    review_section_id = serializers.IntegerField()
    order_num_1 = serializers.IntegerField()
    order_num_2 = serializers.IntegerField()

    def validate(self, data):
        review_section_id = data["review_section_id"]
        order_num_1 = data["order_num_1"]
        order_num_2 = data["order_num_2"]

        # Ensure the ReviewSection exists
        if not ReviewSection.objects.filter(id=review_section_id).exists():
            raise serializers.ValidationError("ReviewSection not found.")

        # Check if order_num_1 and order_num_2 exist in any of the models for the same ReviewSection
        if not self._order_num_exists(review_section_id, order_num_1):
            raise serializers.ValidationError(
                f"Order number {order_num_1} not found in ReviewSection."
            )
        if not self._order_num_exists(review_section_id, order_num_2):
            raise serializers.ValidationError(
                f"Order number {order_num_2} not found in ReviewSection."
            )

        return data

    def _order_num_exists(self, review_section_id, order_num):
        # Check existence of order_num in all three models
        return (
            ReviewText.objects.filter(
                review_section_id=review_section_id, order_num=order_num
            ).exists()
            or ReviewPhoto.objects.filter(
                review_section_id=review_section_id, order_num=order_num
            ).exists()
            or ReviewVideo.objects.filter(
                review_section_id=review_section_id, order_num=order_num
            ).exists()
        )
