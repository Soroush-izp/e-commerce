from django.contrib import admin
from .models import (
    Brand, BrandPhoto, BrandVideo, AttributeType, AttributeGroup, ProductAttributeValue,
    Category, Product, ProductDetail, ProductPhoto, ProductVideo, ProductSKU, ProductSKUAttribute,
    ReviewSection, ReviewText, ReviewPhoto, ReviewVideo
)


# Inline admin classes for related objects
class BrandPhotoInline(admin.TabularInline):
    model = BrandPhoto
    extra = 1


class BrandVideoInline(admin.TabularInline):
    model = BrandVideo
    extra = 1


class ProductPhotoInline(admin.TabularInline):
    model = ProductPhoto
    extra = 1


class ProductVideoInline(admin.TabularInline):
    model = ProductVideo
    extra = 1


class ReviewTextInline(admin.TabularInline):
    model = ReviewText
    extra = 1


class ReviewPhotoInline(admin.TabularInline):
    model = ReviewPhoto
    extra = 1


class ReviewVideoInline(admin.TabularInline):
    model = ReviewVideo
    extra = 1


# Custom ModelAdmin classes
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand_name', 'is_active')
    search_fields = ('brand_name',)
    inlines = [BrandPhotoInline, BrandVideoInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'level', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active', 'level')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active')
    search_fields = ('name', 'category__name')
    list_filter = ('is_active', 'category')
    inlines = [ProductPhotoInline, ProductVideoInline]


class ProductSKUAdmin(admin.ModelAdmin):
    list_display = ('sku', 'product', 'price', 'quantity', 'is_active')
    search_fields = ('sku', 'product__name')
    list_filter = ('is_active',)


class ReviewSectionAdmin(admin.ModelAdmin):
    list_display = ('product', 'title', 'order_num')
    inlines = [ReviewTextInline, ReviewPhotoInline, ReviewVideoInline]


# Register models with customized admin classes
admin.site.register(Brand, BrandAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductSKU, ProductSKUAdmin)
admin.site.register(ReviewSection, ReviewSectionAdmin)

# Register models without custom admin classes
admin.site.register(BrandPhoto)
admin.site.register(BrandVideo)
admin.site.register(AttributeType)
admin.site.register(AttributeGroup)
admin.site.register(ProductAttributeValue)
admin.site.register(ProductDetail)
admin.site.register(ProductPhoto)
admin.site.register(ProductVideo)
admin.site.register(ProductSKUAttribute)
admin.site.register(ReviewText)
admin.site.register(ReviewPhoto)
admin.site.register(ReviewVideo)
