from django.urls import path
from .views import *

urlpatterns = [
    # Payment APIs for users
    # Create a payment request for a specific order (POST)
    # This API initiates a payment process for a given order by creating a payment request.
    path("request/", PaymentRequestView.as_view(), name="payment-request"),
    # Verify the payment status using the authority code after Zarinpal callback (GET)
    # This API verifies the payment's success or failure by using the authority code returned by Zarinpal after a payment attempt.
    path("verify/", PaymentVerifyView.as_view(), name="payment-verify"),
    # List all payments made by the authenticated user (GET)
    # This API returns a history of all payments made by the logged-in user, ordered by the most recent payment.
    path("history/", PaymentHistoryView.as_view(), name="payment-history"),
    # Retrieve details of a specific payment by ID (GET)
    # This API provides detailed information about a specific payment made by the authenticated user, identified by its ID.
    path("<int:pk>/", PaymentDetailView.as_view(), name="payment-detail"),
    # Payment APIs for admins
    # List all payments in the system for admin users (GET)
    # This API allows admin users to view all payments in the system, ordered by the most recent payment.
    path(
        "admin/payments/",
        AdminPaymentHistoryView.as_view(),
        name="admin-payment-history",
    ),
    # Retrieve details of a specific payment by ID for admin users (GET)
    # This API allows admin users to view detailed information about a specific payment, identified by its ID.
    path(
        "admin/payments/<int:pk>/",
        AdminPaymentDetailView.as_view(),
        name="admin-payment-detail",
    ),
]
