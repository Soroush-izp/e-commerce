from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema, extend_schema_field
from rest_framework.views import APIView
from django.conf import settings
from .models import PaymentDetails
from orders.models import OrderDetails
from .serializers import PaymentDetailsSerializer
import requests
from rest_framework import status, serializers


@extend_schema(
    methods=["POST"],
    summary="Create or Update Payment Request",
    description="Create or update a payment request for a specific order. This process redirects the user to Zarinpal for payment.",
    request=PaymentDetailsSerializer,
    tags=["Payments"]
)
class PaymentRequestView(APIView):
    """
    Create or update a payment request for a specific order and redirect to Zarinpal payment page.
    """
    serializer_class = PaymentDetailsSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        order_id = request.data.get('order')

        # Retrieve the order and ensure it belongs to the user
        try:
            order = OrderDetails.objects.get(id=order_id, user=user)
        except OrderDetails.DoesNotExist:
            return Response({'order': 'Order does not exist or does not belong to the current user.'}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the order is valid for payment
        if order.status not in ['pending', 'failed']:
            return Response({'order': 'Order is not in a valid state for payment.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a PaymentDetails instance already exists for this order
        payment = PaymentDetails.objects.filter(order=order).first()

        if payment:
            # Update the existing payment instance
            payment.amount = order.total
            payment.status = 'pending'  # Reset the status to pending
            payment.authority = None  # Clear the authority for a new payment request
            payment.save()
        else:
            # Create a new payment instance
            payment_data = {
                'user': user.id,
                'amount': order.total,
                'order': order.id
            }
            serializer = self.serializer_class(data=payment_data)
            if serializer.is_valid():
                payment = serializer.save()

        # Send the payment request to Zarinpal
        data = {
            'merchant_id': settings.ZARINPAL_MERCHANT_ID,
            'currency': 'IRT',  # 'IRT' for tomans, 'IRR' for rials
            'amount': payment.amount,
            'description': f'Payment for Order {payment.order.id}',
            'callback_url': settings.ZARINPAL_CALLBACK_URL,
        }
        try:
            response = requests.post(settings.ZARINPAL_REQUEST_URL, json=data)
            response_data = response.json()

            if response_data.get('data', {}).get('code') == 100:
                # Store the authority code and save
                payment.authority = response_data['data']['authority']
                payment.save()
            else:
                return Response({'error': 'Payment request failed', 'details': response_data.get('errors', {})}, status=status.HTTP_400_BAD_REQUEST)
        except requests.RequestException as e:
            return Response({'error': 'Failed to connect to payment gateway', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Return the Zarinpal URL for payment
        zarinpal_url = f"{settings.ZARINPAL_STARTPAY_URL}{payment.authority}"
        return Response({'url': zarinpal_url}, status=status.HTTP_201_CREATED)


@extend_schema(
    methods=["GET"],
    summary="Verify Payment",
    description="Verify the status of a payment after a callback from Zarinpal. The authority parameter is required.",
    tags=["Payments"]
)
class PaymentVerifyView(RetrieveAPIView):
    """
    Verify the payment status after Zarinpal callback.
    """
    queryset = PaymentDetails.objects.all()
    serializer_class = PaymentDetailsSerializer

    def get(self, request, *args, **kwargs):
        authority = request.query_params.get('Authority')
        if not authority:
            return Response({'error': 'Authority parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        payment = self.queryset.filter(authority=authority).first()
        if not payment:
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)

        # Prepare data for Zarinpal verification
        data = {
            'merchant_id': settings.ZARINPAL_MERCHANT_ID,
            'amount': int(float(payment.amount)),
            'authority': authority,
        }
        try:
            response = requests.post(settings.ZARINPAL_VERIFY_URL, json=data)
            response_data = response.json()

            # Handle the response from Zarinpal
            if response_data.get('data', {}).get('code') == 100:
                payment.status = 'successful'
                payment.ref_id = response_data['data']['ref_id']
                payment.save()
                
                # Update the product quantities for the associated order
                order = payment.order
                if order:
                    order_items = order.items.all()
                    for item in order_items:
                        sku = item.product_sku
                        if sku.quantity >= item.quantity:  # Check stock availability
                            sku.quantity -= item.quantity  # Deduct ordered quantity
                            sku.save()
                        else:
                            return Response({
                                'error': f"Insufficient stock for {sku.sku}",
                                'available_quantity': sku.quantity,
                            }, status=status.HTTP_400_BAD_REQUEST)
                
                return Response(self.serializer_class(payment).data, status=status.HTTP_200_OK)
            else:
                payment.status = 'failed'
                payment.save()
                return Response({
                    'error': 'Payment verification failed',
                    'details': response_data.get('data', {}).get('message', 'Unknown error'),
                }, status=status.HTTP_400_BAD_REQUEST)

        except requests.RequestException as e:
            return Response({'error': 'Failed to connect to payment gateway', 'details': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except KeyError:
            return Response({'error': 'Unexpected response from payment gateway'}, status=status.HTTP_502_BAD_GATEWAY)


@extend_schema(
    methods=["GET"],
    summary="List User Payments",
    description="Retrieve a list of all payments made by the authenticated user, ordered by the latest payment date.",
    tags=["Payments"]
)
class PaymentHistoryView(ListAPIView):
    """
    Retrieve a list of all payments made by the authenticated user.
    """
    serializer_class = PaymentDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PaymentDetails.objects.filter(user=self.request.user).order_by('-created_at')


@extend_schema(
    methods=["GET"],
    summary="Retrieve Payment Details",
    description="Retrieve detailed information about a specific payment made by the authenticated user.",
    tags=["Payments"]
)
class PaymentDetailView(RetrieveAPIView):
    """
    Retrieve details of a specific payment by ID.
    """
    queryset = PaymentDetails.objects.all()
    serializer_class = PaymentDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


@extend_schema(
    methods=["GET"],
    summary="List All Payments (Admin)",
    description="Retrieve a list of all payments in the system. Accessible only to admin users.",
    tags=["Payments (Admin)"]
)

class AdminPaymentHistoryView(ListAPIView):
    """
    Retrieve a list of all payments for admin users.
    """
    queryset = PaymentDetails.objects.all().order_by('-created_at')
    serializer_class = PaymentDetailsSerializer
    permission_classes = [IsAdminUser]


@extend_schema(
    methods=["GET"],
    summary="Retrieve Payment Details (Admin)",
    description="Retrieve detailed information about a specific payment. Accessible only to admin users.",
    tags=["Payments (Admin)"]
)
class AdminPaymentDetailView(RetrieveAPIView):
    """
    Retrieve details of a specific payment by ID for admin users.
    """
    queryset = PaymentDetails.objects.all()
    serializer_class = PaymentDetailsSerializer
    permission_classes = [IsAdminUser]
