from rest_framework import serializers

from .models import PaymentHistory


class PaymentHistorySerializer(serializers.ModelSerializer):
    transaction_status = serializers.SerializerMethodField()
    billing_type = serializers.SerializerMethodField()

    class Meta:
        model = PaymentHistory
        fields = (
            'order',
            'due_date',
            'amount',
            'split_condictions',
            'billing_type',
            'transaction_status',
            'transaction_code'
        )

    def get_transaction_status(self, obj):
        return obj.get_transaction_status_display()

    def get_billing_type(self, obj):
        return obj.get_billing_type_display()


