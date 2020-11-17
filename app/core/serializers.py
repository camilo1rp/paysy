from abc import ABC

from rest_framework import serializers

from core.models import Customer, Transaction


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class TransactionSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()

    class Meta:
        model = Transaction
        fields = ('id_pago', 'total', 'tax', 'pay_details', 'customer')


class ZonaPagosStartPaymentSerializer(serializers.Serializer):
    """Serialize the starting payment API for Zona Pagos"""
    email = serializers.EmailField(max_length=255)
    document_type = serializers.CharField(max_length=255)
    document = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=127)
    surname = serializers.CharField(max_length=127)
    phone = serializers.IntegerField()
    extra_field_1 = serializers.CharField(max_length=127, allow_blank=True)
    extra_field_2 = serializers.CharField(max_length=127, allow_blank=True)
    extra_field_3 = serializers.CharField(max_length=127, allow_blank=True)
    extra_field_4 = serializers.CharField(max_length=127, allow_blank=True)
    extra_field_5 = serializers.CharField(max_length=127, allow_blank=True)
    id_pago = serializers.CharField(max_length=255)
    pay_gateway = serializers.IntegerField()
    details = serializers.CharField(max_length=511, allow_blank=True)
    value = serializers.DecimalField(default=0.00,
                                     max_digits=10,
                                     decimal_places=2,
                                     required=False)
    tax = serializers.DecimalField(default=0.00,
                                   max_digits=10,
                                   decimal_places=2,
                                   required=False)
    total = serializers.DecimalField(default=0.00,
                                     max_digits=10,
                                     decimal_places=2,
                                     required=False)
    pay_details = serializers.CharField(max_length=511)
