from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.exceptions import ValidationError  # Import ValidationError
from django.db import transaction  # Import transaction
from accounts.manager import IsSuperUser  # custom permission
from rest_framework.parsers import MultiPartParser, FormParser  # for parsing file
from drf_spectacular.utils import extend_schema, extend_schema_field, OpenApiParameter
from rest_framework import status
from drf_spectacular.types import OpenApiTypes
from .models import *
from .serializers import *
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


# # Brand Views
@extend_schema(
    methods=["GET"],
    summary="List Active Brands",
    description="Retrieve a list of all active brands for users.",
    tags=["Brands"],
)
class BrandListView(generics.ListAPIView):
    serializer_class = BrandSerializer

    def get_queryset(self):
        # Filter the queryset to only include active brands for user
        return Brand.objects.filter(is_active=True)


@extend_schema(
    methods=["GET"],
    summary="Admin List Brands",
    description="List all brands for admin users.",
    tags=["Brands"],
)
@extend_schema(
    methods=["POST"],
    summary="Admin Create Brand",
    description="Allow admin to create a new brand.",
    request=BrandSerializer,
    tags=["Brands"],
)
class BrandListCreateView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminUser | IsSuperUser]


@extend_schema(
    methods=["GET"],
    summary="Retrieve Brand Details",
    description="Retrieve details of a specific brand, including associated photos and videos, for users.",
    tags=["Brands"],
)
class BrandShowDetailView(generics.RetrieveAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandDetailSerializer  # Using BrandDetailSerializer to include photos and videos


@extend_schema(
    methods=["GET"],
    summary="Admin Retrieve Brand",
    description="Admin can retrieve a specific brand, including its associated photos and videos.",
    tags=["Brands"],
)
@extend_schema(
    methods=["PUT", "PATCH"],
    summary="Admin Update Brand",
    description="Admin can update details of a specific brand, including its associated photos and videos.",
    request=BrandDetailSerializer,
    tags=["Brands"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Admin Delete Brand",
    description="Admin can delete a specific brand, including its associated photos and videos.",
    tags=["Brands"],
)
class BrandDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandDetailSerializer
    permission_classes = [IsAdminUser | IsSuperUser]


@extend_schema(
    methods=["GET"],
    summary="List Brand Photos",
    description="List all brand photos.",
    tags=["BrandPhotos"],
)
@extend_schema(
    methods=["POST"],
    summary="Create Brand Photo",
    description="Admin can create a new brand photo.",
    request=BrandPhotoSerializer,
    tags=["BrandPhotos"],
)
class BrandPhotoListCreateView(generics.ListCreateAPIView):
    queryset = BrandPhoto.objects.all()
    serializer_class = BrandPhotoSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]
    parser_classes = (MultiPartParser, FormParser)


@extend_schema(
    methods=["GET"],
    summary="Retrieve Brand Photo",
    description="Retrieve a specific brand photo.",
    tags=["BrandPhotos"],
)
@extend_schema(
    methods=["PUT", "PATCH"],
    summary="Update Brand Photo",
    description="Admin can update a specific brand photo.",
    request=BrandPhotoSerializer,
    tags=["BrandPhotos"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Delete Brand Photo",
    description="Admin can delete a specific brand photo.",
    tags=["BrandPhotos"],
)
class BrandPhotoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BrandPhoto.objects.all()
    serializer_class = BrandPhotoSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]
    parser_classes = (MultiPartParser, FormParser)


@extend_schema(
    methods=["GET"],
    summary="List Brand Videos",
    description="List all brand videos.",
    tags=["BrandVideos"],
)
@extend_schema(
    methods=["POST"],
    summary="Create Brand Video",
    description="Admin can create a new brand video.",
    request=BrandVideoSerializer,
    tags=["BrandVideos"],
)
class BrandVideoListCreateView(generics.ListCreateAPIView):
    queryset = BrandVideo.objects.all()
    serializer_class = BrandVideoSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]
    parser_classes = (MultiPartParser, FormParser)


@extend_schema(
    methods=["GET"],
    summary="Retrieve Brand Video",
    description="Retrieve a specific brand video.",
    tags=["BrandVideos"],
)
@extend_schema(
    methods=["PUT", "PATCH"],
    summary="Update Brand Video",
    description="Admin can update a specific brand video.",
    request=BrandVideoSerializer,
    tags=["BrandVideos"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Delete Brand Video",
    description="Admin can delete a specific brand video.",
    tags=["BrandVideos"],
)
class BrandVideoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BrandVideo.objects.all()
    serializer_class = BrandVideoSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]
    parser_classes = (MultiPartParser, FormParser)


# # Attribute Views
@extend_schema(
    methods=["GET"],
    summary="Retrieve Attribute Type",
    description="Admin can retrieve a specific attribute type.",
    tags=["AttributeTypes"],
)
@extend_schema(
    methods=["PUT", "PATCH"],
    summary="Update Attribute Type",
    description="Admin can update a specific attribute type.",
    request=AttributeTypeSerializer,
    tags=["AttributeTypes"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Delete Attribute Type",
    description="Admin can delete a specific attribute type.",
    tags=["AttributeTypes"],
)
class AttributeTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AttributeType.objects.all()
    serializer_class = AttributeTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]

    def perform_destroy(self, instance):
        # Find all AttributeGroup instances where the attribute is used
        related_groups = AttributeGroup.objects.filter(attributes=instance)

        # Remove the attribute from each related AttributeGroup
        for group in related_groups:
            group.attributes.remove(instance)

        # After removing it from the related groups, delete the AttributeType instance
        instance.delete()


@extend_schema(
    methods=["GET"],
    summary="List Attribute Types",
    description="List all attribute types.",
    tags=["AttributeTypes"],
)
@extend_schema(
    methods=["POST"],
    summary="Create Attribute Type",
    description="Admin can create a new attribute type.",
    request=AttributeTypeSerializer,
    tags=["AttributeTypes"],
)
class AttributeTypeListCreateView(generics.ListCreateAPIView):
    queryset = AttributeType.objects.all()
    serializer_class = AttributeTypeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]


@extend_schema(
    methods=["GET"],
    summary="Retrieve Attribute Group",
    description="Admin can retrieve a specific attribute group.",
    tags=["AttributeGroups"],
)
@extend_schema(
    methods=["PUT", "PATCH"],
    summary="Update Attribute Group",
    description="Admin can update a specific attribute group.",
    request=AttributeGroupSerializer,
    tags=["AttributeGroups"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Delete Attribute Group",
    description="Admin can delete a specific attribute group.",
    tags=["AttributeGroups"],
)
class AttributeGroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AttributeGroup.objects.all()
    serializer_class = AttributeGroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]


@extend_schema(
    methods=["GET"],
    summary="List Attribute Groups",
    description="List all attribute groups.",
    tags=["AttributeGroups"],
)
@extend_schema(
    methods=["POST"],
    summary="Create Attribute Group",
    description="Admin can create a new attribute group.",
    request=AttributeGroupSerializer,
    tags=["AttributeGroups"],
)
class AttributeGroupListCreateView(generics.ListCreateAPIView):
    queryset = AttributeGroup.objects.all()
    serializer_class = AttributeGroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]


@extend_schema(
    methods=["GET"],
    summary="Retrieve Product Attribute Value",
    description="Admin can retrieve a specific product attribute value.",
    tags=["ProductAttributeValues"],
)
@extend_schema(
    methods=["PUT", "PATCH"],
    summary="Update Product Attribute Value",
    description="Admin can update a specific product attribute value.",
    request=ProductAttributeValueSerializer,
    tags=["ProductAttributeValues"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Delete Product Attribute Value",
    description="Admin can delete a specific product attribute value.",
    tags=["ProductAttributeValues"],
)
class ProductAttributeValueDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductAttributeValue.objects.all()
    serializer_class = ProductAttributeValueSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]


@extend_schema(
    methods=["GET"],
    summary="List Product Attribute Values",
    description="List all product attribute values.",
    tags=["ProductAttributeValues"],
)
@extend_schema(
    methods=["POST"],
    summary="Create Product Attribute Value",
    description="Admin can create a new product attribute value.",
    request=ProductAttributeValueSerializer,
    tags=["ProductAttributeValues"],
)
class ProductAttributeValueListCreateView(generics.ListCreateAPIView):
    queryset = ProductAttributeValue.objects.all()
    serializer_class = ProductAttributeValueSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]


@extend_schema(
    methods=["GET"],
    summary="List Product Attribute Values",
    description="List all product attribute values.",
    tags=["ProductAttributeValues"],
)
class ProductAttributeValueListView(generics.ListAPIView):
    serializer_class = ProductAttributeValueSerializer
    permission_classes = [
        IsAuthenticated,
        IsAdminUser | IsSuperUser,
    ]  # Adjust as necessary

    def get_queryset(self):
        attribute_type_id = self.kwargs.get("attribute_type_id")
        return ProductAttributeValue.objects.filter(
            type_id=attribute_type_id, is_active=True
        )


# # Category Views
# Retrieve, update, and delete a specific Category for admin
@extend_schema(
    methods=["GET"],
    summary="Admin Retrieve Category",
    description="Admin can retrieve the details of a specific category.",
    tags=["Categories"],
)
@extend_schema(
    methods=["PUT", "PATCH"],
    summary="Admin Update Category",
    description="Admin can update the details of a specific category.",
    request=AdminCategorySerializer,
    tags=["Categories"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Admin Delete Category",
    description="Admin can delete a specific category, specify subcategories have delete with queryparam ?cascade=True or False",
    tags=["Categories"],
)
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = AdminCategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]
    parser_classes = (MultiPartParser, FormParser)


# List and create Categories for admin
@extend_schema(
    methods=["GET"],
    summary="Admin List Categories",
    description="Admin can retrieve a list of all categories.",
    tags=["Categories"],
)
@extend_schema(
    methods=["POST"],
    summary="Admin Create Category",
    description="Admin can create a new category.",
    request=AdminCategorySerializer,
    tags=["Categories"],
)
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = AdminCategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]
    parser_classes = (MultiPartParser, FormParser)


# Views for users to list and retrieve categories
@extend_schema(
    methods=["GET"],
    summary="User List Categories",
    description="Retrieve a list of categories available to users.",
    tags=["Categories"],
)
class UserCategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = UserCategoryListSerializer
    permission_classes = [AllowAny]


@extend_schema(
    methods=["GET"],
    summary="User Retrieve Category Detail",
    description="Retrieve the details of a specific category.",
    tags=["Categories"],
)
class UserCategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = UserCategoryDetailSerializer
    permission_classes = [AllowAny]


# View for nested categories (hierarchical list)
@extend_schema(
    methods=["GET"],
    summary="User List Categories in Hierarchical Structure",
    description="Retrieve categories in a hierarchical structure (parent-child).",
    tags=["Categories"],
)
class CategoryTreeView(generics.ListAPIView):
    queryset = Category.objects.filter(parent=None, is_active=True)
    serializer_class = CategoryTreeSerializer
    permission_classes = [AllowAny]


# # Product Views
# Public view to list all active products for users
@extend_schema(
    methods=["GET"],
    summary="List all active products",
    description="Retrieve a list of all active products that are available for the public.",
    tags=["Public Products"],
)
@method_decorator(cache_page(60 * 15), name="dispatch")
class PublicProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)  # Filter for active products
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]  # Allow all users


# Admin view to list all products and manage the active status
@extend_schema(
    methods=["GET"],
    summary="Admin List Products",
    description="Allows admins to list all products for management.",
    tags=["Admin Products"],
)
@extend_schema(
    methods=["POST"],
    summary="Admin Toggle Product Active Status",
    description="Allows admins to reverse the is_active status of a specified product.",
    request=ProductListSerializer,
    tags=["Admin Products"],
)
class AdminProductListManageView(generics.GenericAPIView):
    queryset = Product.objects.all()  # Show all products without filtering
    serializer_class = ProductListSerializer
    permission_classes = [
        IsAuthenticated,
        IsAdminUser | IsSuperUser,
    ]  # Only accessible to authenticated admins

    def get(self, request, *args, **kwargs):
        """List all products for the admin."""
        products = self.get_queryset()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Reverse the is_active status of a specified product."""
        product_id = request.data.get("id")
        try:
            product = Product.objects.get(id=product_id)
            product.is_active = not product.is_active
            product.save()
            serializer = self.get_serializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND
            )


# Public view to retrieve a specific active product for users
@extend_schema(
    methods=["GET"],
    summary="Retrieve a specific active product",
    description="Get the details of a specific active product by its ID.",
    tags=["Public Products"],
)
class UserProductView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)  # Only active products
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


# Admin view for retrieving, updating, or deleting a specific product
@extend_schema(
    methods=["GET"],
    summary="Admin Retrieve Product",
    description="Allows admins to retrieve a specific product by its ID.",
    tags=["Admin Products"],
)
@extend_schema(
    methods=["PATCH"],
    summary="Admin Partially Update Product",
    description="Allows admins to partially update an existing product by its ID.",
    request=ProductSerializer,
    tags=["Admin Products"],
)
@extend_schema(
    methods=["PUT"],
    summary="Admin Update Product",
    description="Allows admins to update an existing product by its ID.",
    request=ProductSerializer,
    tags=["Admin Products"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Admin Delete Product",
    description="Allows admins to delete a specific product by its ID.",
    tags=["Admin Products"],
)
class AdminProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]
    parser_classes = (MultiPartParser, FormParser)

    def get(self, request, *args, **kwargs):
        """Retrieve a product by ID."""
        return super().get(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Partially update an existing product by ID."""
        return super().patch(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Update an existing product by ID."""
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete a product by ID."""
        return super().delete(request, *args, **kwargs)


# Admin view for creating a new product
@extend_schema(
    methods=["POST"],
    summary="Admin create a new product",
    description="Allows admins to create a new product.",
    tags=["Admin Products"],
    request=ProductSerializer,
)
class AdminProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        """Create a new product."""
        return super().post(request, *args, **kwargs)


# # Product Detail Views
# Public view to retrieve the details of a specific product detail
@extend_schema(
    methods=["GET"],
    summary="Retrieve product detail",
    description="lists all ProductDetail items for a given product ID, ordered by order_num..",
    tags=["Product Details"],
)
class PublicProductDetailView(generics.ListAPIView):
    # queryset = ProductDetail.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # Get product_id from the request and filter ProductDetail instances by it
        product_id = self.kwargs.get("product_id")
        return ProductDetail.objects.filter(product_id=product_id).order_by("order_num")


# Admin view to list, create, or update product details
@extend_schema(
    methods=["GET"],
    summary="Admin List Product Details",
    description="Allows admin users to list all product details.",
    tags=["Admin Product Details"],
)
@extend_schema(
    methods=["POST"],
    summary="Admin Create Product Detail",
    description="Allows admin users to create a new product detail.",
    request=ProductDetailSerializer,
    tags=["Admin Product Details"],
)
class AdminProductDetailListCreateView(generics.ListCreateAPIView):
    queryset = ProductDetail.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]


# Admin view to retrieve, update, or delete a specific product detail
@extend_schema(
    methods=["GET"],
    summary="Admin Retrieve Product Detail",
    description="Allows admin users to retrieve a specific product detail by its ID.",
    tags=["Admin Product Details"],
)
@extend_schema(
    methods=["PATCH"],
    summary="Admin Partially Update Product Detail",
    description="Allows admin users to partially update a specific product detail by its ID.",
    request=ProductDetailSerializer,
    tags=["Admin Product Details"],
)
@extend_schema(
    methods=["PUT"],
    summary="Admin Update Product Detail",
    description="Allows admin users to update a specific product detail by its ID.",
    request=ProductDetailSerializer,
    tags=["Admin Product Details"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Admin Delete Product Detail",
    description="Allows admin users to delete a specific product detail by its ID.",
    tags=["Admin Product Details"],
)
class AdminProductChangeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductDetail.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]


# View to swap the order of two ProductDetail instances
@extend_schema(
    methods=["POST"],
    summary="Swap order of two product details",
    description="Swaps the order number of two ProductDetail instances.",
    tags=["Product Details"],
)
class ProductDetailSwapOrderView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]
    serializer_class = ProductDetailOrderUpdateSerializer

    def post(self, request, *args, **kwargs):
        first_detail_id = request.data.get("first_detail_id")
        second_detail_id = request.data.get("second_detail_id")

        if not first_detail_id or not second_detail_id:
            return Response(
                {"error": "Both ProductDetail IDs must be provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            first_detail = ProductDetail.objects.get(id=first_detail_id)
            second_detail = ProductDetail.objects.get(id=second_detail_id)
        except ProductDetail.DoesNotExist:
            return Response(
                {"error": "One or both ProductDetail instances not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Check if both ProductDetail instances belong to the same product
        if first_detail.product_id != second_detail.product_id:
            return Response(
                {"error": "Both ProductDetails must belong to the same product."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Swap the order_num values using a temporary placeholder
        with transaction.atomic():
            temp_order_num = (
                max(  # biggest order_num + 1
                    ProductDetail.objects.filter(
                        product_id=first_detail.product_id
                    ).values_list("order_num", flat=True)
                )
                + 1
            )

            # Step 1: Set first_detail's order_num to the temporary value
            first_detail_order_num = first_detail.order_num
            first_detail.order_num = temp_order_num
            first_detail.save()

            # Step 2: Set second_detail's order_num to original first_detail's order_num
            second_detail_order_num = second_detail.order_num
            second_detail.order_num = first_detail_order_num
            second_detail.save()

            # Step 3: Set first_detail's order_num to original second_detail's order_num
            first_detail.order_num = second_detail_order_num
            first_detail.save()

        # Serialize the updated ProductDetail instances
        first_serializer = self.get_serializer(first_detail)
        second_serializer = self.get_serializer(second_detail)

        return Response(
            {
                "first_detail": first_serializer.data,
                "second_detail": second_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


@extend_schema(
    methods=["PUT", "PATCH"],
    summary="Batch update product details order",
    description="Allows admin users to batch update the order numbers of multiple ProductDetail instances for a specific product. If some ProductDetail records are not included in the updates, they will be deleted.",
    tags=["Admin Product Details"],
)
class ProductDetailBatchUpdateView(generics.UpdateAPIView):
    queryset = ProductDetail.objects.all()
    serializer_class = ProductDetailBatchUpdateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]

    def update(self, request, *args, **kwargs):
        # Initialize the serializer with the input data
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Perform the batch update using the serializer's update method
            serializer.update(None, serializer.validated_data)
            # Return a success response
            return Response(
                {"message": "Batch update successful."}, status=status.HTTP_200_OK
            )

        # If validation fails, return an error response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Public view to list all photos related to a specific product
@extend_schema(
    methods=["GET"],
    summary="List product photos",
    description="Retrieve all photos associated with a specific product.",
    tags=["Product Media"],
)
class PublicProductPhotoListView(generics.ListAPIView):
    serializer_class = ProductPhotoSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        product_id = self.kwargs.get("product_id")
        return ProductPhoto.objects.filter(product_id=product_id)


# Admin view to create a new photo for a product
@extend_schema(
    methods=["POST"],
    summary="Admin create product photo",
    description="Allows admin users to create a new photo for a specific product.",
    tags=["Admin Product Media"],
)
class AdminProductPhotoCreateView(generics.CreateAPIView):
    queryset = ProductPhoto.objects.all()
    serializer_class = ProductPhotoSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]
    parser_classes = (MultiPartParser, FormParser)


# Admin view to retrieve, update, partially update, or delete a specific product photo
@extend_schema(
    methods=["GET"],
    summary="Admin Retrieve Product Photo",
    description="Allows admin users to retrieve a specific product photo.",
    tags=["Admin Product Media"],
)
@extend_schema(
    methods=["PUT"],
    summary="Admin Update Product Photo",
    description="Allows admin users to update a specific product photo.",
    request=ProductPhotoSerializer,
    tags=["Admin Product Media"],
)
@extend_schema(
    methods=["PATCH"],
    summary="Admin Partially Update Product Photo",
    description="Allows admin users to partially update a specific product photo.",
    request=ProductPhotoSerializer,
    tags=["Admin Product Media"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Admin Delete Product Photo",
    description="Allows admin users to delete a specific product photo.",
    tags=["Admin Product Media"],
)
class AdminProductPhotoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductPhoto.objects.all()
    serializer_class = ProductPhotoSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        """
        Fetch the ProductPhoto instance by ID and ensure it belongs to the specified product.
        """
        product_id = self.kwargs.get("product_id")
        photo_id = self.kwargs.get("pk")
        try:
            # Get the product photo for the given product
            return ProductPhoto.objects.get(product_id=product_id, id=photo_id)
        except ProductPhoto.DoesNotExist:
            # If the product photo does not exist, return a 404 response
            raise Response(
                {"error": "Product photo not found."}, status=status.HTTP_404_NOT_FOUND
            )


# Public view to list all videos related to a specific product
@extend_schema(
    methods=["GET"],
    summary="List product videos",
    description="Retrieve all videos associated with a specific product.",
    tags=["Product Media"],
)
class PublicProductVideoListView(generics.ListAPIView):
    serializer_class = ProductVideoSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        product_id = self.kwargs.get("product_id")
        return ProductVideo.objects.filter(product_id=product_id)


# Admin view to create a new video for a product
@extend_schema(
    methods=["POST"],
    summary="Admin create product video",
    description="Allows admin users to create a new video for a specific product.",
    tags=["Admin Product Media"],
)
class AdminProductVideoCreateView(generics.CreateAPIView):
    queryset = ProductVideo.objects.all()
    serializer_class = ProductVideoSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]


# Admin view to retrieve, update, partially update, or delete a specific product video
@extend_schema(
    methods=["GET"],
    summary="Admin Retrieve Product Video",
    description="Allows admin users to retrieve a specific product video.",
    tags=["Admin Product Media"],
)
@extend_schema(
    methods=["PUT"],
    summary="Admin Update Product Video",
    description="Allows admin users to update a specific product video.",
    request=ProductVideoSerializer,
    tags=["Admin Product Media"],
)
@extend_schema(
    methods=["PATCH"],
    summary="Admin Partially Update Product Video",
    description="Allows admin users to partially update a specific product video.",
    request=ProductVideoSerializer,
    tags=["Admin Product Media"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Admin Delete Product Video",
    description="Allows admin users to delete a specific product video.",
    tags=["Admin Product Media"],
)
class AdminProductVideoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductVideo.objects.all()
    serializer_class = ProductVideoSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        """
        Fetch the ProductVideo instance by ID and ensure it belongs to the specified product.
        """
        product_id = self.kwargs.get("product_id")
        video_id = self.kwargs.get("pk")
        try:
            # Get the product video for the given product
            return ProductVideo.objects.get(product_id=product_id, id=video_id)
        except ProductVideo.DoesNotExist:
            # If the product video does not exist, return a 404 response
            raise Response(
                {"error": "Product video not found."}, status=status.HTTP_404_NOT_FOUND
            )


# Admin: List all SKUs or create a new SKU. Requires authentication and admin/superuser permissions.
@extend_schema(
    methods=["GET"],
    summary="List all SKUs",
    description="Retrieve a list of all SKUs.",
    tags=["Product SKU Management"],
)
@extend_schema(
    methods=["POST"],
    summary="Create a new SKU",
    description="Create a new SKU with the provided data. Admin access required.",
    request=ProductSKUSerializer,
    tags=["Product SKU Management"],
)
class ProductSKUListView(generics.ListCreateAPIView):
    queryset = ProductSKU.objects.all()
    serializer_class = ProductSKUSerializer
    # permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]

    def perform_create(self, serializer):
        serializer.save()

    def get_permissions(self):
        if self.request.method == "POST":
            # Require authentication and admin or superuser permissions for POST (create) requests
            return [IsAuthenticated, IsAdminUser | IsSuperUser]
        # Allow any user to view the SKU list
        return [AllowAny()]


# Admin: Retrieve, update, or delete a specific SKU by ID. Requires authentication and admin/superuser permissions.
@extend_schema(
    methods=["GET"],
    summary="Retrieve a specific SKU",
    description="Retrieve the details of a specific SKU by its ID. Admin access required.",
    tags=["Product SKU Management"],
)
@extend_schema(
    methods=["PUT"],
    summary="Update a specific SKU",
    description="Update the details of a specific SKU by its ID. Admin access required.",
    request=ProductSKUSerializer,
    tags=["Product SKU Management"],
)
@extend_schema(
    methods=["PATCH"],
    summary="Partially update a specific SKU",
    description="Partially update fields of a specific SKU by its ID. Admin access required.",
    request=ProductSKUSerializer,
    tags=["Product SKU Management"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Delete a specific SKU",
    description="Delete a specific SKU by its ID. Admin access required.",
    tags=["Product SKU Management"],
)
class ProductSKUDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductSKU.objects.all()
    serializer_class = ProductSKUSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]


# User: Retrieve a list of SKUs for a specific product. Admin permissions are not required.
@extend_schema(
    methods=["GET"],
    summary="List SKUs for a specific product",
    description="Retrieve a list of SKUs associated with a specific product by product ID.",
    tags=["Product SKU Management"],
)
class ListProductSKUView(generics.ListAPIView):
    queryset = ProductSKU.objects.all()
    serializer_class = ProductSKUSerializer

    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )

        skus = ProductSKU.objects.filter(product=product)
        serializer = self.get_serializer(skus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Admin: List all SKU attributes or create a new SKU attribute. Requires authentication and admin/superuser permissions.
@extend_schema(
    methods=["GET"],
    summary="List all SKU attributes",
    description="Retrieve a list of all SKU attributes.",
    tags=["Product SKU Attribute Management"],
)
@extend_schema(
    methods=["POST"],
    summary="Create a new SKU attribute",
    description="Create a new SKU attribute with the provided data. Admin access required.",
    request=ProductSKUAttributeSerializer,
    tags=["Product SKU Attribute Management"],
)
class ProductSKUAttributeListCreateView(generics.ListCreateAPIView):
    """
    Admin: Retrieve all SKU attributes (GET) or create a new SKU attribute (POST).
    User: Retrieve all SKU attributes (GET).
    """

    queryset = ProductSKUAttribute.objects.all()
    serializer_class = ProductSKUAttributeSerializer
    # permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]

    def get_permissions(self):
        if self.request.method == "POST":
            # Require authentication and admin or superuser permissions for POST requests
            return [
                IsAuthenticated(),
                IsAdminUser(),
            ]  # Instantiate each permission class
        # Allow any user to view the SKU list
        return [AllowAny()]


# Admin: Retrieve, update, or delete a specific SKU attribute by ID. Requires authentication and admin/superuser permissions.
@extend_schema(
    methods=["GET"],
    summary="Retrieve a specific SKU attribute",
    description="Retrieve the details of a specific SKU attribute by its ID. Admin access required.",
    tags=["Product SKU Attribute Management"],
)
@extend_schema(
    methods=["PUT"],
    summary="Update a specific SKU attribute",
    description="Update the details of a specific SKU attribute by its ID. Admin access required.",
    request=ProductSKUAttributeSerializer,
    tags=["Product SKU Attribute Management"],
)
@extend_schema(
    methods=["PATCH"],
    summary="Partially update a specific SKU attribute",
    description="Partially update fields of a specific SKU attribute by its ID. Admin access required.",
    request=ProductSKUAttributeSerializer,
    tags=["Product SKU Attribute Management"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Delete a specific SKU attribute",
    description="Delete a specific SKU attribute by its ID. Admin access required.",
    tags=["Product SKU Attribute Management"],
)
class ProductSKUAttributeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Admin: Retrieve, update, or delete a specific SKU attribute.
    User: Retrieve a specific SKU attribute (GET).
    """

    queryset = ProductSKUAttribute.objects.all()
    serializer_class = ProductSKUAttributeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]


#       Review Views
# Admin: List all review sections or create a new review section. Requires authentication and admin/superuser permissions.
@extend_schema(
    methods=["GET"],
    summary="List all review sections",
    description="Retrieve a list of all review sections.",
    tags=["Review Section Management"],
)
@extend_schema(
    methods=["POST"],
    summary="Create a new review section",
    description="Create a new review section with the provided data.",
    request=ReviewSectionSerializer,
    tags=["Review Section Management"],
)
class ReviewSectionListCreateView(generics.ListCreateAPIView):
    """
    API view to list and create ReviewSection instances.
    """

    queryset = ReviewSection.objects.all()
    serializer_class = ReviewSectionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]


# Admin: Retrieve, update, or delete a specific review section by ID. Requires authentication and admin/superuser permissions.
@extend_schema(
    methods=["GET"],
    summary="Retrieve a specific review section",
    description="Retrieve the details of a specific review section by its ID.",
    tags=["Review Section Management"],
)
@extend_schema(
    methods=["PUT"],
    summary="Update a specific review section",
    description="Update the details of a specific review section by its ID.",
    request=ReviewSectionDetailSerializer,
    tags=["Review Section Management"],
)
@extend_schema(
    methods=["PATCH"],
    summary="Partially update a specific review section",
    description="Partially update fields of a specific review section by its ID.",
    request=ReviewSectionDetailSerializer,
    tags=["Review Section Management"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Delete a specific review section",
    description="Delete a specific review section by its ID.",
    tags=["Review Section Management"],
)
class ReviewSectionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, and delete a specific ReviewSection.
    """

    queryset = ReviewSection.objects.all()
    serializer_class = ReviewSectionDetailSerializer
    permission_classes = [IsAuthenticated, IsAdminUser | IsSuperUser]


# Admin: List review sections by product ID. Requires authentication and admin/superuser permissions.
@extend_schema(
    methods=["GET"],
    summary="List review sections by product",
    description="Retrieve a list of review sections for a specific product.",
    parameters=[
        OpenApiParameter(
            name="product_id",
            location=OpenApiParameter.PATH,
            description="Product ID",
            required=True,
            type=int,
        )
    ],
    tags=["Review Section Management"],
)
class ReviewSectionListByProductView(generics.ListAPIView):
    serializer_class = ReviewSectionDetailSerializer

    def get_queryset(self):
        # Retrieve the product ID from the URL and filter ReviewSection by product
        product_id = self.kwargs.get("product_id")
        return ReviewSection.objects.filter(product_id=product_id).order_by("order_num")


# Admin: List all review texts or create a new review text. Requires authentication and admin/superuser permissions.
@extend_schema(
    methods=["GET"],
    summary="List all review texts",
    description="Retrieve a list of all review texts.",
    tags=["Review Text Management"],
)
@extend_schema(
    methods=["POST"],
    summary="Create a new review text",
    description="Create a new review text with the provided data.",
    request=ReviewTextSerializer,
    tags=["Review Text Management"],
)
class ReviewTextListCreateView(generics.ListCreateAPIView):
    """
    API view to list and create ReviewText instances.
    """

    queryset = ReviewText.objects.all()
    serializer_class = ReviewTextSerializer


# Admin: Retrieve, update, or delete a specific review text by ID. Requires authentication and admin/superuser permissions.
@extend_schema(
    methods=["GET"],
    summary="Retrieve a specific review text",
    description="Retrieve the details of a specific review text by its ID.",
    tags=["Review Text Management"],
)
@extend_schema(
    methods=["PUT"],
    summary="Update a specific review text",
    description="Update the details of a specific review text by its ID.",
    request=ReviewTextSerializer,
    tags=["Review Text Management"],
)
@extend_schema(
    methods=["PATCH"],
    summary="Partially update a specific review text",
    description="Partially update fields of a specific review text by its ID.",
    request=ReviewTextSerializer,
    tags=["Review Text Management"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Delete a specific review text",
    description="Delete a specific review text by its ID.",
    tags=["Review Text Management"],
)
class ReviewTextDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, and delete a specific ReviewText.
    """

    queryset = ReviewText.objects.all()
    serializer_class = ReviewTextSerializer


# Admin: List all review photos or create a new review photo. Requires authentication and admin/superuser permissions.
@extend_schema(
    methods=["GET"],
    summary="List all review photos",
    description="Retrieve a list of all review photos.",
    tags=["Review Photo Management"],
)
@extend_schema(
    methods=["POST"],
    summary="Create a new review photo",
    description="Create a new review photo with the provided data.",
    request=ReviewPhotoSerializer,
    tags=["Review Photo Management"],
)
class ReviewPhotoListCreateView(generics.ListCreateAPIView):
    """
    API view to list and create ReviewPhoto instances.
    """

    queryset = ReviewPhoto.objects.all()
    serializer_class = ReviewPhotoSerializer
    parser_classes = (MultiPartParser, FormParser)


# Admin: Retrieve, update, or delete a specific review photo by ID. Requires authentication and admin/superuser permissions.
@extend_schema(
    methods=["GET"],
    summary="Retrieve a specific review photo",
    description="Retrieve the details of a specific review photo by its ID.",
    tags=["Review Photo Management"],
)
@extend_schema(
    methods=["PUT"],
    summary="Update a specific review photo",
    description="Update the details of a specific review photo by its ID.",
    request=ReviewPhotoSerializer,
    tags=["Review Photo Management"],
)
@extend_schema(
    methods=["PATCH"],
    summary="Partially update a specific review photo",
    description="Partially update fields of a specific review photo by its ID.",
    request=ReviewPhotoSerializer,
    tags=["Review Photo Management"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Delete a specific review photo",
    description="Delete a specific review photo by its ID.",
    tags=["Review Photo Management"],
)
class ReviewPhotoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, and delete a specific ReviewPhoto.
    """

    queryset = ReviewPhoto.objects.all()
    serializer_class = ReviewPhotoSerializer
    parser_classes = (MultiPartParser, FormParser)


# Admin: List all review videos or create a new review video. Requires authentication and admin/superuser permissions.
@extend_schema(
    methods=["GET"],
    summary="List all review videos",
    description="Retrieve a list of all review videos.",
    tags=["Review Video Management"],
)
@extend_schema(
    methods=["POST"],
    summary="Create a new review video",
    description="Create a new review video with the provided data.",
    request=ReviewVideoSerializer,
    tags=["Review Video Management"],
)
class ReviewVideoListCreateView(generics.ListCreateAPIView):
    """
    API view to list and create ReviewVideo instances.
    """

    queryset = ReviewVideo.objects.all()
    serializer_class = ReviewVideoSerializer
    parser_classes = (MultiPartParser, FormParser)


# Admin: Retrieve, update, or delete a specific review video by ID. Requires authentication and admin/superuser permissions.
@extend_schema(
    methods=["GET"],
    summary="Retrieve a specific review video",
    description="Retrieve the details of a specific review video by its ID.",
    tags=["Review Video Management"],
)
@extend_schema(
    methods=["PUT"],
    summary="Update a specific review video",
    description="Update the details of a specific review video by its ID.",
    request=ReviewVideoSerializer,
    tags=["Review Video Management"],
)
@extend_schema(
    methods=["PATCH"],
    summary="Partially update a specific review video",
    description="Partially update fields of a specific review video by its ID.",
    request=ReviewVideoSerializer,
    tags=["Review Video Management"],
)
@extend_schema(
    methods=["DELETE"],
    summary="Delete a specific review video",
    description="Delete a specific review video by its ID.",
    tags=["Review Video Management"],
)
class ReviewVideoDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, and delete a specific ReviewVideo.
    """

    queryset = ReviewVideo.objects.all()
    serializer_class = ReviewVideoSerializer
    parser_classes = (MultiPartParser, FormParser)


# Admin: Swap order numbers of two review sections by their IDs. Requires authentication and admin/superuser permissions.
@extend_schema(
    methods=["POST"],
    summary="Swap order numbers of two review sections",
    description="Swap the order numbers of two review sections by their IDs.",
    request=SwapOrderNumSerializer,
    tags=["Review Section Management"],
)
class SwapOrderNumView(generics.GenericAPIView):
    """
    Generic view to swap the order_num of two ReviewSection instances given their IDs.
    Ensures both ReviewSections belong to the same product.
    """

    serializer_class = SwapOrderNumSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            id1 = serializer.validated_data["id1"]
            id2 = serializer.validated_data["id2"]

            # Get the two ReviewSection instances
            try:
                obj1 = ReviewSection.objects.get(id=id1)
                obj2 = ReviewSection.objects.get(id=id2)
            except ReviewSection.DoesNotExist:
                return Response(
                    {"error": "One or both ReviewSection instances not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Check if both belong to the same product
            if obj1.product_id != obj2.product_id:
                return Response(
                    {
                        "error": "ReviewSection instances do not belong to the same product."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Swap the order_num values using a temporary placeholder to avoid conflict
            with transaction.atomic():
                temp_order_num = (
                    max(
                        ReviewSection.objects.filter(
                            product_id=obj1.product_id
                        ).values_list("order_num", flat=True)
                    )
                    + 1
                )

                # Step 1: Set obj1's order_num to the temporary value
                obj1_order_num = obj1.order_num
                obj1.order_num = temp_order_num
                obj1.save()

                # Step 2: Set obj2's order_num to obj1's original order_num
                obj2_order_num = obj2.order_num
                obj2.order_num = obj1_order_num
                obj2.save()

                # Step 3: Set obj1's order_num to obj2's original order_num
                obj1.order_num = obj2_order_num
                obj1.save()

            # Serialize the updated instances
            obj1_data = ReviewSectionSerializer(obj1).data
            obj2_data = ReviewSectionSerializer(obj2).data

            return Response(
                {
                    "message": "Order numbers swapped successfully",
                    "obj1": obj1_data,
                    "obj2": obj2_data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Admin: Swap order numbers of two review items by their IDs. Requires authentication and admin/superuser permissions.
@extend_schema(
    methods=["POST"],
    summary="Swap order numbers of two review items",
    description="Swap the order numbers of two review items by their IDs.",
    request=SwapOrderNumItemsSerializer,
    tags=["Review Item Management"],
)
class SwapOrderNumItemView(generics.GenericAPIView):
    """
    Swap order_num between two sets of items across ReviewText, ReviewPhoto, and ReviewVideo.
    """

    serializer_class = SwapOrderNumItemsSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        review_section_id = serializer.validated_data["review_section_id"]
        order_num_1 = serializer.validated_data["order_num_1"]
        order_num_2 = serializer.validated_data["order_num_2"]

        with transaction.atomic():
            # Use a temporary value larger than any existing order_num
            max_order_num = self._get_max_order_num(review_section_id)
            temp_order_num = max_order_num + 1

            # Swap order_num for each model
            self._swap_order(
                ReviewText, review_section_id, order_num_1, order_num_2, temp_order_num
            )
            self._swap_order(
                ReviewPhoto, review_section_id, order_num_1, order_num_2, temp_order_num
            )
            self._swap_order(
                ReviewVideo, review_section_id, order_num_1, order_num_2, temp_order_num
            )

        return Response(
            {"message": "Order numbers swapped successfully."},
            status=status.HTTP_200_OK,
        )

    def _get_max_order_num(self, review_section_id):
        """
        Get the maximum order_num across all models for the given ReviewSection.
        """
        max_text = (
            ReviewText.objects.filter(review_section_id=review_section_id).aggregate(
                models.Max("order_num")
            )["order_num__max"]
            or 0
        )
        max_photo = (
            ReviewPhoto.objects.filter(review_section_id=review_section_id).aggregate(
                models.Max("order_num")
            )["order_num__max"]
            or 0
        )
        max_video = (
            ReviewVideo.objects.filter(review_section_id=review_section_id).aggregate(
                models.Max("order_num")
            )["order_num__max"]
            or 0
        )

        return max(max_text, max_photo, max_video)

    def _swap_order(
        self, model, review_section_id, order_num_1, order_num_2, temp_order_num
    ):
        """
        Swap order_num for a given model within the same ReviewSection.
        """
        # Step 1: Move order_num_1 to a temporary value
        model.objects.filter(
            review_section_id=review_section_id, order_num=order_num_1
        ).update(order_num=temp_order_num)

        # Step 2: Move order_num_2 to order_num_1
        model.objects.filter(
            review_section_id=review_section_id, order_num=order_num_2
        ).update(order_num=order_num_1)

        # Step 3: Move the temporary value to order_num_2
        model.objects.filter(
            review_section_id=review_section_id, order_num=temp_order_num
        ).update(order_num=order_num_2)
