from django.db import models
from decimal import Decimal
import uuid  # Import the uuid module
from django.core.validators import FileExtensionValidator, MinValueValidator
from .mixins import *
import mimetypes
from django.core.exceptions import ValidationError
from base.models import TimestampedModel  # Add this import


# Brand models
class Brand(models.Model):
    brand_name = models.CharField(
        max_length=100, unique=True
    )  # Ensure brand names are unique
    description = models.TextField(blank=True, null=True)
    website = models.URLField(max_length=200)  # URL field for the brand's website
    instagram = models.URLField(max_length=200, blank=True, null=True)
    facebook = models.URLField(max_length=200, blank=True, null=True)
    icon = models.ImageField(upload_to="brand/brand_icons/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.brand_name


class BrandPhoto(models.Model):  # This contains photos of each brand
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="photos")
    alt = models.TextField()
    photo = models.ImageField(upload_to="brand/brand_photos/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.brand.brand_name}"  # Corrected from self.brand.name


class BrandVideo(models.Model):  # This contains videos of each brand
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="videos")
    alt = models.TextField()
    video = models.FileField(
        upload_to="brand/brand_videos/",
        validators=[
            FileExtensionValidator(allowed_extensions=["mp4", "mov", "avi", "mkv"])
        ],
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video for {self.brand.brand_name}"  # Corrected from self.brand.name

    def clean(self):
        super().clean()
        mime_type, encoding = mimetypes.guess_type(self.video.name)
        if mime_type and not mime_type.startswith("video"):
            raise ValidationError("Uploaded file is not a valid video.")


# Attribute models
class AttributeType(models.Model):  # Define dynamic attribute types (e.g., size, color)
    name = models.CharField(
        max_length=100
    )  # Name of the attribute (e.g., 'Color', 'Size')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AttributeGroup(models.Model):
    """Defines groups of attributes (e.g., Size & Color group, etc.)"""

    name = models.CharField(max_length=100)  # Group name (e.g., 'Clothing Attributes')
    attributes = models.ManyToManyField(
        AttributeType, related_name="groups"
    )  # Associate with multiple AttributeTypes
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ProductAttributeValue(models.Model):
    type = models.ForeignKey(
        AttributeType, on_delete=models.CASCADE, related_name="attributes"
    )
    value = models.JSONField(max_length=100)  # Supports strings, integers, floats, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.type.name}: {self.value}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["type", "value"], name="unique_type_value")
        ]


class Category(models.Model):
    """Categories can have parent-child relationships and use their own and parent attribute groups"""

    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="subcategories",
        blank=True,
        null=True,
        default=None,
    )
    name = models.CharField(max_length=80, unique=True)
    attribute_groups = models.ManyToManyField(
        AttributeGroup, related_name="categories"
    )  # Each category has its own groups
    photo = models.ImageField(
        upload_to="category/category_photos/", blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)
    level = models.PositiveIntegerField(default=0)  # Automatically managed level
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Override save method to calculate and set category level based on parent, and propagate attribute groups to subcategories."""
        if self.parent:
            self.level = self.parent.level + 1
        else:
            self.level = 0

        # Save the category first
        super().save(*args, **kwargs)

        # After saving, propagate the attribute groups to subcategories
        self.propagate_attribute_groups_to_subcategories()

    def propagate_attribute_groups_to_subcategories(self):
        """Propagate this category's attribute groups to all subcategories."""
        # Get all subcategories
        subcategories = self.subcategories.all()

        # Get current attribute groups of the parent category
        inherited_groups = list(self.attribute_groups.all())

        for subcategory in subcategories:
            # Sync subcategory attribute groups with the parent's attribute groups
            subcategory.attribute_groups.set(inherited_groups)

            # Recursively propagate the changes to further nested subcategories
            subcategory.save()

    def get_all_attribute_groups(self):
        """Fetch this category's attribute groups, plus parent categories' attribute groups, ensuring uniqueness."""
        groups = set(self.attribute_groups.all())
        if self.parent:
            parent_groups = self.parent.get_all_attribute_groups()
            groups.update(parent_groups)
        return list(groups)


# Product models
class Product(TimestampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    summary = models.TextField()  # Assuming different roles from description
    cover = models.ImageField(
        upload_to="product/product_covers/", blank=True, null=True
    )  # Allow blank/nullable
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["is_active"]),
            models.Index(fields=["created_at"]),
        ]


class ProductDetail(models.Model):  # This contains details of each product
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="details"
    )
    title = models.CharField(max_length=50)
    value = models.TextField()
    order_num = models.PositiveIntegerField()  # New field for ordering

    class Meta:
        # Ensure that order_num is unique per product
        unique_together = ("product", "order_num")

    def __str__(self):
        return f"{self.product.name} - {self.title}: {self.value}"


class ProductPhoto(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="photos"
    )
    alt = models.TextField()
    photo = models.ImageField(upload_to="product/product_photos/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.product.name}"


class ProductVideo(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="videos"
    )
    alt = models.TextField()
    video = models.FileField(
        upload_to="product/product_videos/",
        validators=[
            FileExtensionValidator(allowed_extensions=["mp4", "mov", "avi", "mkv"])
        ],
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Video for {self.product.name}"

    def clean(self):
        super().clean()
        mime_type, encoding = mimetypes.guess_type(self.video.name)
        if mime_type and not mime_type.startswith("video"):
            raise ValidationError("Uploaded file is not a valid video.")


class ProductSKU(
    TimestampedModel
):  # SKU specifies price, quantity based on product attributes
    sku = models.CharField(
        max_length=100, unique=True, editable=False
    )  # Unique ID for each SKU
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="skus")
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(
        validators=[MinValueValidator(0)]
    )  # Prevent negative quantity
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.sku:
            # Generate a unique SKU if it doesn't exist
            self.sku = f"SKU-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"SKU: {self.sku}, Product: {self.product.name}"

    class Meta:
        indexes = [
            models.Index(fields=["sku"]),
            models.Index(fields=["quantity"]),
            models.Index(fields=["is_active"]),
        ]


class ProductSKUAttribute(models.Model):
    sku = models.ForeignKey(
        ProductSKU, on_delete=models.CASCADE, related_name="sku_attributes"
    )
    attribute_value = models.ForeignKey(ProductAttributeValue, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            "sku",
            "attribute_value",
        )  # Prevent duplicate attribute-value pairs for the same SKU

    def __str__(self):
        return f"SKU: {self.sku.sku}, Attribute: {self.attribute_value.type.name}, Value: {self.attribute_value.value}"


# Review models
class ReviewSection(ReviewOrderMixin):  # ReviewSection model
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="review"
    )
    title = models.CharField(max_length=255)

    class Meta:
        unique_together = ("product", "order_num")  # Ensure unique order per product

    def __str__(self):
        return f"ReviewSection {self.order_num} for {self.product.name}"


class ReviewText(ReviewOrderItemMixin):  # ReviewText model
    review_section = models.ForeignKey(
        ReviewSection, on_delete=models.CASCADE, related_name="texts"
    )
    text = models.TextField()

    def __str__(self):
        return f"Text for ReviewSection {self.review_section.order_num}"

    class Meta(ReviewOrderItemMixin.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=["review_section", "order_num"],
                name="unique_order_num_per_text_section",
            )
        ]


class ReviewPhoto(ReviewOrderItemMixin):  # ReviewPhoto model
    review_section = models.ForeignKey(
        ReviewSection, on_delete=models.CASCADE, related_name="photos"
    )
    image = models.ImageField(upload_to="review_photos/")

    CENTER_LARGE = "center-large"
    LEFT_SMALL = "left-small"
    RIGHT_SMALL = "right-small"

    POSITION_CHOICES = [
        (CENTER_LARGE, "CenterLarge"),
        (LEFT_SMALL, "LeftSmall"),
        (RIGHT_SMALL, "RightSmall"),
    ]
    position = models.CharField(max_length=30, choices=POSITION_CHOICES)

    def __str__(self):
        return f"Photo for ReviewSection {self.review_section.order_num}"

    class Meta(ReviewOrderItemMixin.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=["review_section", "order_num"],
                name="unique_order_num_per_photo_section",
            )
        ]


class ReviewVideo(ReviewOrderItemMixin):  # ReviewVideo model
    review_section = models.ForeignKey(
        ReviewSection, on_delete=models.CASCADE, related_name="videos"
    )
    video = models.FileField(
        upload_to="review_videos/",
        validators=[
            FileExtensionValidator(allowed_extensions=["mp4", "mov", "avi", "mkv"])
        ],
    )

    def __str__(self):
        return f"Video for ReviewSection {self.review_section.order_num}"

    def clean(self):
        super().clean()
        mime_type, encoding = mimetypes.guess_type(self.video.name)
        if mime_type and not mime_type.startswith("video"):
            raise ValidationError("Uploaded file is not a valid video.")

    class Meta(ReviewOrderItemMixin.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=["review_section", "order_num"],
                name="unique_order_num_per_video_section",
            )
        ]
