import pprint
from datetime import datetime
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, status

from financial.models import PaymentHistory, Order
from financial.serializers import PaymentHistorySerializer
from users.models import User
from django.shortcuts import get_object_or_404
from competitor.models import Registration
from .utils import get_payment_status


class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = PaymentHistorySerializer
    queryset = PaymentHistory.objects.all()

    def create(self, request, *args, **kwargs):
        reference_id = request.data['reference_id']
        status_pagseguro = request.data['charges'][0]['status']
        status = get_payment_status(status_pagseguro)
        if status == 'CONFIRMED':
            Order.objects.filter(registration__registration_number=reference_id).update(status=2)
            Registration.objects.filter(registration_number=reference_id).update(payment_status=True)
        payment = PaymentHistory.objects.filter(order__registration__registration_number=reference_id).last()

        if not payment:
            registration = get_object_or_404(Registration, registration_number=reference_id)
            order = get_object_or_404(Order, registration=registration)
            payment = PaymentHistory.objects.create(
                order=order,
                amount=request.data['charges'][0]['amount']['value'],
                transaction_status=status
            )

        payment.transaction_status = status
        payment.invoice_number = request.data['id']
        payment.billing_type = request.data['charges'][0]['payment_method']['type']

        try:
            payment.split_condictions = request.data['charges'][0]['payment_method']['installments']
        except KeyError:
            pass

        payment.qrcode_image = request.data['qr_code'][0]['links'][0]['href']
        payment.qrcode_key = request.data['qr_code'][0]['links'][1]['href']

        data_str = request.data['charges'][0]['paid_at']
        data_obj = datetime.strptime(data_str, "%Y-%m-%dT%H:%M:%S.%f%z")
        payment.due_date = data_obj.strftime("%Y-%m-%d")
        payment.save()

        return JsonResponse({'success': True})
