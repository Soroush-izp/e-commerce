from django.db import models
from rest_framework.exceptions import ValidationError  # Import ValidationError


class ReviewOrderMixin(models.Model):
    # this class use for give order to order_num
    order_num = models.PositiveIntegerField()

    class Meta:
        abstract = True
        ordering = ["order_num"]

    def save(self, *args, **kwargs):
        if not self.order_num:
            # Automatically set the order number if it's not set
            last_order = self.__class__.objects.filter().order_by("order_num").last()
            if last_order:
                self.order_num = last_order.order_num + 1
            else:
                self.order_num = 1
        super().save(*args, **kwargs)


class ReviewOrderItemMixin(models.Model):
    order_num = models.PositiveIntegerField(
        null=True
    )  # Allow null temporarily for auto-assignment

    class Meta:
        abstract = True
        ordering = ["order_num"]

    def save(self, *args, **kwargs):
        # Set order_num if not provided
        if self.order_num is None:
            self.assign_order_num()
        # Validate unique order_num across all models for the same review_section
        self.validate_unique_order_num()
        super().save(*args, **kwargs)

    def assign_order_num(self):
        from .models import (
            ReviewText,
            ReviewPhoto,
            ReviewVideo,
        )  # Avoid circular imports

        # Get maximum order_num used in the same review_section across all models
        max_order_text = (
            ReviewText.objects.filter(review_section=self.review_section).aggregate(
                models.Max("order_num")
            )["order_num__max"]
            or 0
        )
        max_order_photo = (
            ReviewPhoto.objects.filter(review_section=self.review_section).aggregate(
                models.Max("order_num")
            )["order_num__max"]
            or 0
        )
        max_order_video = (
            ReviewVideo.objects.filter(review_section=self.review_section).aggregate(
                models.Max("order_num")
            )["order_num__max"]
            or 0
        )

        # Assign the next available order_num
        self.order_num = max(max_order_text, max_order_photo, max_order_video) + 1

    def validate_unique_order_num(self):
        from .models import (
            ReviewText,
            ReviewPhoto,
            ReviewVideo,
        )  # Avoid circular imports

        # Check if order_num already exists in other models for the same review_section
        existing_text = (
            ReviewText.objects.filter(
                review_section=self.review_section, order_num=self.order_num
            ).exists()
            if not isinstance(self, ReviewText)
            else False
        )

        existing_photo = (
            ReviewPhoto.objects.filter(
                review_section=self.review_section, order_num=self.order_num
            ).exists()
            if not isinstance(self, ReviewPhoto)
            else False
        )

        existing_video = (
            ReviewVideo.objects.filter(
                review_section=self.review_section, order_num=self.order_num
            ).exists()
            if not isinstance(self, ReviewVideo)
            else False
        )

        if existing_text or existing_photo or existing_video:
            raise ValidationError(
                f"The order number {self.order_num} is already taken for this review section."
            )
