import requests
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import viewsets, views, status
from rest_framework.views import APIView

from core.models import Transaction, PayGateWay, Customer, ZonaPagos, \
    ZonaPagosParamVal, TransactionStatus
from core.serializers import TransactionSerializer, \
    PayGateWaySerializer


class StartPayment(viewsets.ModelViewSet):
    """Manage Api for starting payment"""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        """Create response and add message"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        trans = serializer.save()
        exists = Customer.objects.filter(
            **request.data['customer']
        ).exists()
        if not exists:
            customer = Customer.objects.create(
                **request.data['customer']
            )
        else:
            customer = Customer.objects.get(
                **request.data['customer']
            )
        zona_pagos = ZonaPagos.objects.get(gateway=trans.pay_gateway,
                                           name=trans.config_name)

        payment_payload = {
            "flt_total_con_iva": trans.total,
            "flt_valor_iva": trans.tax,
            "str_id_pago": trans.id_pago,
            "str_descripcion_pago": trans.pay_details,
            "str_email": customer.email,
            "str_id_cliente": str(customer.id),
            "str_tipo_id": customer.document_type,
            "str_nombre_cliente": customer.name,
            "str_apellido_cliente": customer.surname,
            "str_telefono_cliente": str(customer.phone),
            "str_opcional1": customer.extra_field_1,
            "str_opcional2": customer.extra_field_2,
            "str_opcional3": customer.extra_field_3,
            "str_opcional4": customer.extra_field_4,
            "str_opcional5": customer.extra_field_5
        }
        security_payload = {
            "int_id_comercio": zona_pagos.configuration.int_id_comercio,
            "str_usuario": zona_pagos.configuration.str_usuario,
            "str_clave": zona_pagos.configuration.str_clave,
            "int_modalidad": zona_pagos.configuration.int_modalidad
        }
        configuration_payload = []
        params_values = ZonaPagosParamVal.objects.filter(
            zona_pagos=zona_pagos
        )
        for params_val in params_values:
            item = {'int_codigo': params_val.zona_pagos_param.code,
                    'str_valor': params_val.value
                    }
            configuration_payload.append(item)
        payload = {'InformacionPago': payment_payload,
                   'InformacionSeguridad': security_payload,
                   'AdicionalesConfiguracion': configuration_payload
                   }
        url = zona_pagos.configuration.payment_url
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        serialized_json = JSONRenderer().render(payload)
        response = requests.post(url, headers=headers, data=serialized_json)
        data = response.json()
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=response.status_code, headers=headers)


class PayGateWayViewSet(viewsets.ModelViewSet):
    """Manage Api for starting payment"""
    queryset = PayGateWay.objects.all()
    serializer_class = PayGateWaySerializer


class ZonaPagosConfirmView(viewsets.GenericViewSet):
    """Zona pagos view to confirm payments"""

    def list(self, request, *args, **kwargs):
        id_comercio = request.GET.get('id_comercio')
        id_pago = request.GET.get('id_pago')

        if id_pago and id_comercio:
            transaction = Transaction.objects.get(id_pago=id_pago)
            transaction.status = "pending"
            transaction.save()
            TransactionStatus.objects.create(transaction=transaction,
                                             status=transaction.status,
                                             details="pago hecho")
            data = TransactionSerializer(transaction).data
            response = Response(data, status=status.HTTP_200_OK)
            return response
        else:
            response = Response({'error': "check parameters"},
                                status=status.HTTP_400_BAD_REQUEST)
            return response
