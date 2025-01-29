from django.contrib import admin
from .models import PaymentDetails


@admin.register(PaymentDetails)
class PaymentDetailsAdmin(admin.ModelAdmin):
    list_display = ["user", "order", "amount", "status", "created_at"]
    list_filter = ["status", "created_at"]
    search_fields = ["user__username", "order__id", "ref_id"]
