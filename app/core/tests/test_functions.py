import io
import requests

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from core.models import Customer, ZonaPagosConfig, ZonaPagos, \
    ZonaPagosParamVal, PayGateWay, Transaction, ZonaPagosParam

from core.serializers import CustomerSerializer


class FunctionTest(TestCase):

    def setUp(self):
        self.buyer = Customer.objects.create(email='test@paysy.com',
                                             document_type='1',
                                             document='avc1234',
                                             name='name',
                                             surname='surname',
                                             phone=12345678,
                                             extra_field_1="extra 1",
                                             extra_field_2="extra 2",
                                             extra_field_3="extra 3",
                                             extra_field_4="extra 4",
                                             extra_field_5="extra 5"
                                             )
        self.user = get_user_model().objects.create_user(
            email="test@paysy.com",
            password="test123"
        )
        self.gateway = PayGateWay.objects.create(name='testGateway',
                                                 prefix='test')
        self.gateway.site.add(self.user)

        self.transaction = Transaction.objects.create(id_pago='test@paysy.com',
                                                      customer=self.buyer,
                                                      pay_gateway=self.gateway,
                                                      details='transfer '
                                                              'details',
                                                      status='surname',
                                                      value=134.34,
                                                      tax=5.0,
                                                      total=20.5,
                                                      pay_details="payment "
                                                                  "details",
                                                      )
        self.param = ZonaPagosParam.objects.create(code=50,
                                                   description='Código de '
                                                               'servicio '
                                                               'Personal: '
                                                               'Define la '
                                                               'configuración '
                                                               'adicional '
                                                               'que puede '
                                                               'tener '
                                                               'el comercio',
                                                   payment=False
                                                   )
        self.config = ZonaPagosConfig. \
            objects.create(int_id_comercio=30004,
                           id_comercio=30004,
                           str_usuario="Tn30004",
                           str_clave="Tn30004*",
                           int_modalidad=1,
                           payment_url="https://www.zonapagos.com"
                                       "/Apis_CicloPago"
                                       "/api/InicioPago",
                           consult_url="https://www.zonapagos.com"
                                       "/Apis_CicloPago"
                                       "/api "
                                       "/VerificacionPago"
                           )
        self.zona_pagos = ZonaPagos.objects.create(gateway=self.gateway,
                                                   configuration=self.config,
                                                   )
        ZonaPagosParamVal.objects.create(zona_pagos=self.zona_pagos,
                                         zona_pagos_param=self.param,
                                         value="2701")

    def test_serializer_customer(self):
        """Test serializing and deserializing customer"""

        # serializing
        serializer = CustomerSerializer(self.buyer)
        serialized_json = JSONRenderer().render(serializer.data)
        # deserializing
        stream = io.BytesIO(serialized_json)
        data = JSONParser().parse(stream)
        # changing email (it must be unique)
        data['email'] = 'test2@paysy.com'
        serializer2 = CustomerSerializer(data=data)
        serializer2.is_valid()
        serializer2.save()

        exists = Customer.objects.filter(email='test2@paysy.com').exists()
        self.assertTrue(exists)

    def test_consume_zona_pagos_start_payment_api(self):
        """Test starting payment with Zona Pagos"""

        payment_payload = {
            "flt_total_con_iva": self.transaction.total,
            "flt_valor_iva": self.transaction.tax,
            "str_id_pago": self.transaction.id_pago,
            "str_descripcion_pago": self.transaction.pay_details,
            "str_email": self.buyer.email,
            "str_id_cliente": str(self.buyer.id),
            "str_tipo_id": self.buyer.document_type,
            "str_nombre_cliente": self.buyer.name,
            "str_apellido_cliente": self.buyer.surname,
            "str_telefono_cliente": str(self.buyer.phone),
            "str_opcional1": self.buyer.extra_field_1,
            "str_opcional2": self.buyer.extra_field_2,
            "str_opcional3": self.buyer.extra_field_3,
            "str_opcional4": self.buyer.extra_field_4,
            "str_opcional5": self.buyer.extra_field_5
        }
        security_payload = {
            "int_id_comercio": self.config.int_id_comercio,
            "str_usuario": self.config.str_usuario,
            "str_clave": self.config.str_clave,
            "int_modalidad": self.config.int_modalidad
        }
        configuration_payload = []
        params_values = ZonaPagosParamVal.objects.filter(
            zona_pagos=self.zona_pagos
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
        url = self.config.payment_url
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        serialized_json = JSONRenderer().render(payload)
        response = requests.post(url, headers=headers, data=serialized_json)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['int_codigo'], 1)
        self.assertEqual(data['str_cod_error'], "")
        self.assertEqual(data['str_descripcion_error'], "")
        print(data['str_url'])
