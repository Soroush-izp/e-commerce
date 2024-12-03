from rest_framework import serializers
from .models import PaymentDetails

class PaymentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetails
        fields = '__all__'
        read_only_fields = ['authority', 'status', 'ref_id', 'created_at', 'updated_at', 'amount', 'user']
        
    def validate_order(self, value):
        """
        Ensure there is no duplicate payment for the same order.
        """
        user = self.context['request'].user
        if PaymentDetails.objects.filter(order=value, user=user).exists():
            raise serializers.ValidationError("Payment details for this order already exist.")
        return value
