from rest_framework import serializers

from core.models import Customer, Transaction, PayGateWay


class PayGateWaySerializer(serializers.ModelSerializer):
    """Serializer for Customer model"""

    class Meta:
        model = PayGateWay
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model"""

    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {'extra_field_1': {'required': False},
                        'extra_field_2': {'required': False},
                        'extra_field_3': {'required': False},
                        'extra_field_4': {'required': False},
                        'extra_field_5': {'required': False}
                        }


class TransactionSerializer(serializers.ModelSerializer):
    """Serialize Transaction start payment"""
    customer = CustomerSerializer()
    pay_gateway = serializers.PrimaryKeyRelatedField(
        queryset=PayGateWay.objects.all()
    )

    class Meta:
        model = Transaction
        fields = ('id_pago',
                  'details',
                  'total',
                  'tax',
                  'pay_details',
                  'customer',
                  'pay_gateway',
                  'config_name'
                  )
        extra_kwargs = {'details': {'required': False},
                        'value': {'required': False},
                        'tax': {'required': False},
                        'total': {'required': False},
                        }

    def create(self, validated_data):
        """Create customer and transaction instances"""
        customer_data = validated_data.pop('customer')
        customer = Customer.objects.create(**customer_data)
        validated_data['customer'] = customer
        trans = Transaction.objects.create(**validated_data)
        return trans
