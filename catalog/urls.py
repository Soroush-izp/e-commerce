from django.urls import path
from .views import *

urlpatterns = [
    # Brand APIs
    # User: List all active brands (GET)
    path("brands/", BrandListView.as_view(), name="brand-list"),
    # Admin: Retrieve a list of all brands (GET) or create a new brand (POST)
    path("admin/brand/", BrandListCreateView.as_view(), name="brand-create"),
    # User: Retrieve details of a specific brand by ID, including associated photos and videos (GET)
    path("brand/<int:pk>/", BrandShowDetailView.as_view(), name="brand-detail"),
    # Admin: Retrieve (GET), update (PUT, PATCH), or delete (DELETE) a specific brand by ID
    path("admin/brand/<int:pk>/", BrandDetailView.as_view(), name="brand-detail"),
    # Admin: Retrieve a list of all brand photos (GET) or create a new brand photo (POST)
    path(
        "admin/brand-photos/",
        BrandPhotoListCreateView.as_view(),
        name="brandphoto-list-create",
    ),
    # Admin: Retrieve (GET), update (PUT, PATCH), or delete (DELETE) a specific brand photo by ID
    path(
        "admin/brand-photos/<int:pk>/",
        BrandPhotoDetailView.as_view(),
        name="brandphoto-detail",
    ),
    # Admin: Retrieve a list of all brand videos (GET) or create a new brand video (POST)
    path(
        "admin/brand-videos/",
        BrandVideoListCreateView.as_view(),
        name="brandvideo-list-create",
    ),
    # Admin: Retrieve (GET), update (PUT, PATCH), or delete (DELETE) a specific brand video by ID
    path(
        "admin/brand-videos/<int:pk>/",
        BrandVideoDetailView.as_view(),
        name="brandvideo-detail",
    ),
    # AttributeType URLs
    # Admin: Retrieve a list of all attribute types (GET) or create a new attribute type (POST)
    path(
        "admin/attribute-types/",
        AttributeTypeListCreateView.as_view(),
        name="attribute-type-list-create",
    ),
    # Admin: Retrieve (GET), update (PUT, PATCH), or delete (DELETE) a specific attribute type by ID
    path(
        "admin/attribute-type/<int:pk>/",
        AttributeTypeDetailView.as_view(),
        name="attribute-type-detail",
    ),
    # Retrieve a list of all attribute values associated with a specific attribute type by its ID
    path(
        "attribute-values/<int:attribute_type_id>/",
        ProductAttributeValueListView.as_view(),
        name="attribute-value-list",
    ),
    # AttributeGroup URLs
    # Admin: Retrieve a list of all attribute groups (GET) or create a new attribute group (POST)
    path(
        "admin/attribute-groups/",
        AttributeGroupListCreateView.as_view(),
        name="attribute-group-list-create",
    ),
    # Admin: Retrieve (GET), update (PUT, PATCH), or delete (DELETE) a specific attribute group by ID
    path(
        "admin/attribute-group/<int:pk>/",
        AttributeGroupDetailView.as_view(),
        name="attribute-group-detail",
    ),
    # ProductAttributeValue URLs
    # Admin: Retrieve a list of all product attribute values (GET) or create a new product attribute value (POST)
    path(
        "admin/product-attribute-values/",
        ProductAttributeValueListCreateView.as_view(),
        name="product-attribute-value-list-create",
    ),
    # Admin: Retrieve (GET), update (PUT, PATCH), or delete (DELETE) a specific product attribute value by ID
    path(
        "admin/product-attribute-value/<int:pk>/",
        ProductAttributeValueDetailView.as_view(),
        name="product-attribute-value-detail",
    ),
    # Category URLs
    # Admin: Retrieve a list of all categories (GET) or create a new category (POST)
    path(
        "admin/categories/",
        CategoryListCreateView.as_view(),
        name="category-list-create",
    ),
    # Admin: Retrieve (GET), update (PUT, PATCH), or delete (DELETE) a specific category by ID
    path(
        "admin/category/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"
    ),
    # User: Retrieve a list of all active categories (GET)
    path("categories/", UserCategoryListView.as_view(), name="user-category-list"),
    # User: Retrieve details of a specific category by ID (GET)
    path(
        "category/<int:pk>/",
        UserCategoryDetailView.as_view(),
        name="user-category-detail",
    ),
    # User: Retrieve a hierarchical structure of all categories, including subcategories (GET)
    path("categories/tree/", CategoryTreeView.as_view(), name="category-tree"),
    # Product APIs
    # User: Retrieve a list of all public products (GET)
    path("products-list/", PublicProductListView.as_view(), name="public-product-list"),
    # Admin: Retrieve a list of all products for management purposes (GET)
    path(
        "admin/products-list/",
        AdminProductListManageView.as_view(),
        name="admin-product-manage",
    ),
    # User: Retrieve details of a specific product by ID (GET)
    path(
        "product/product-detail/<int:pk>/",
        UserProductView.as_view(),
        name="product-detail",
    ),
    # Admin: Create a new product (POST)
    path(
        "admin/products/", AdminProductCreateView.as_view(), name="admin-product-create"
    ),
    # Admin: Retrieve (GET), update (PUT, PATCH), or delete (DELETE) a specific product by ID
    path(
        "admin/products/<int:pk>/",
        AdminProductDetailView.as_view(),
        name="admin-product-detail",
    ),
    # Product Detail APIs
    # Public: Retrieve details of a specific product by product ID (GET)
    path(
        "product-detail/<int:product_id>/",
        PublicProductDetailView.as_view(),
        name="public-product-detail",
    ),
    # Admin: Retrieve a list of all product details (GET) or create a new product detail (POST)
    path(
        "admin/product-details/",
        AdminProductDetailListCreateView.as_view(),
        name="admin-product-detail-list-create",
    ),
    # Admin: Retrieve (GET), update (PUT, PATCH), or delete (DELETE) a specific product detail by ID
    path(
        "admin/product-detail/<int:pk>/",
        AdminProductChangeDetailView.as_view(),
        name="admin-product-detail",
    ),
    # Admin: Swap the order of two product detail instances (POST)
    path(
        "admin/product-detail/swap-order/",
        ProductDetailSwapOrderView.as_view(),
        name="product-detail-swap-order",
    ),
    # Admin: Batch update the order of multiple product detail instances (POST)
    path(
        "admin/product-detail/batch-update/",
        ProductDetailBatchUpdateView.as_view(),
        name="product-detail-batch-update",
    ),
    # Public: Retrieve a list of all photos associated with a specific product (GET)
    path(
        "product/<int:product_id>/photos/",
        PublicProductPhotoListView.as_view(),
        name="public-product-photo-list",
    ),
    # Admin: Create a new photo for a specific product (POST)
    path(
        "admin/product-photo/create/",
        AdminProductPhotoCreateView.as_view(),
        name="admin-product-photo-create",
    ),
    # Admin: Retrieve (GET), update (PUT, PATCH), or delete (DELETE) a specific photo for a product
    path(
        "admin/product/<int:product_id>/photo/<int:pk>/",
        AdminProductPhotoDetailView.as_view(),
        name="admin-product-photo-detail",
    ),
    # Public: Retrieve a list of all videos associated with a specific product (GET)
    path(
        "product/<int:product_id>/videos/",
        PublicProductVideoListView.as_view(),
        name="public-product-video-list",
    ),
    # Admin: Create a new video for a specific product (POST)
    path(
        "admin/product-video/create/",
        AdminProductVideoCreateView.as_view(),
        name="admin-product-video-create",
    ),
    # Admin: Retrieve (GET), update (PUT, PATCH), or delete (DELETE) a specific video for a product
    path(
        "admin/product/<int:product_id>/video/<int:pk>/",
        AdminProductVideoDetailView.as_view(),
        name="admin-product-video-detail",
    ),
    # ProductSKU URLs
    # Admin: Retrieve a list of all SKUs for all products (GET)
    path("admin/skus/", ProductSKUListView.as_view(), name="product-sku-list"),
    # Admin: Retrieve (GET), update (PUT, PATCH), or delete (DELETE) a specific SKU by ID
    path(
        "admin/skus/<int:pk>/",
        ProductSKUDetailView.as_view(),
        name="product-sku-detail",
    ),
    # Public: Retrieve a list of SKUs for a specific product by product ID (GET)
    path(
        "products/<int:product_id>/skus/",
        ListProductSKUView.as_view(),
        name="create-product-skus",
    ),
    # List all SKU attributes (admin can also create)
    path(
        "sku-attributes/",
        ProductSKUAttributeListCreateView.as_view(),
        name="sku-attribute-list-create",
    ),
    # Retrieve, update, or delete a specific SKU attribute by ID
    path(
        "sku-attributes/<int:pk>/",
        ProductSKUAttributeDetailView.as_view(),
        name="sku-attribute-detail",
    ),
    # ReviewSection URLs
    # Public: List and create review sections for products (GET, POST)
    path(
        "reviews/sections/",
        ReviewSectionListCreateView.as_view(),
        name="review-section-list-create",
    ),
    # Retrieve, update, or delete a specific review section by ID (GET, PUT, PATCH, DELETE)
    path(
        "reviews/sections/<int:pk>/",
        ReviewSectionDetailView.as_view(),
        name="review-section-detail",
    ),
    # Public: List review sections for a specific product, ordered by 'order_num' (GET)
    path(
        "reviews/products/<int:product_id>/sections/",
        ReviewSectionListByProductView.as_view(),
        name="review-section-list-by-product",
    ),
    # Admin: Swap order numbers between review sections for custom ordering (POST)
    path(
        "reviews/sections/swap-order/",
        SwapOrderNumView.as_view(),
        name="review-section-swap-order",
    ),
    # Admin: Swap order numbers between items (text, photo, video) within a review section (POST)
    path(
        "review-section/items/swap-order-num/",
        SwapOrderNumItemView.as_view(),
        name="swap_order_num",
    ),
    # ReviewSection Text URLs
    # Public: List and create text entries for product reviews (GET, POST)
    path(
        "reviews/texts/",
        ReviewTextListCreateView.as_view(),
        name="review-text-list-create",
    ),
    # Retrieve, update, or delete a specific review text entry by ID (GET, PUT, PATCH, DELETE)
    path(
        "reviews/texts/<int:pk>/",
        ReviewTextDetailView.as_view(),
        name="review-text-detail",
    ),
    # ReviewSection photos URLs
    # Public: List and upload photo entries for product reviews (GET, POST)
    path(
        "reviews/photos/",
        ReviewPhotoListCreateView.as_view(),
        name="review-photo-list-create",
    ),
    # Retrieve, update, or delete a specific review photo entry by ID (GET, PUT, PATCH, DELETE)
    path(
        "reviews/photos/<int:pk>/",
        ReviewPhotoDetailView.as_view(),
        name="review-photo-detail",
    ),
    # ReviewSection videos URLs
    # Public: List and upload video entries for product reviews (GET, POST)
    path(
        "reviews/videos/",
        ReviewVideoListCreateView.as_view(),
        name="review-video-list-create",
    ),
    # Retrieve, update, or delete a specific review video entry by ID (GET, PUT, PATCH, DELETE)
    path(
        "reviews/videos/<int:pk>/",
        ReviewVideoDetailView.as_view(),
        name="review-video-detail",
    ),
]
