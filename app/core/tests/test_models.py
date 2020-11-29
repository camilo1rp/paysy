from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Customer, ZonaPagosConfig, ZonaPagos, ZonaPagosParamVal

from core.models import PayGateWay

from core.models import Transaction

from core.models import ZonaPagosParam


class ModelTests(TestCase):

    def create_customer(self):
        """creates and returns a new custom"""
        buyer = Customer.objects.create(email='test@paysy.com',
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
        return buyer

    def create_transaction(self):
        """creates and retirns a new transaction"""
        buyer = self.create_customer()
        user = get_user_model().objects.create_user(
            email="test@paysy.com",
            password="test123"
        )
        gateway = PayGateWay.objects.create(name='testGateway',
                                            prefix='test')
        gateway.site.add(user)
        transaction = Transaction.objects.create(id_pago='test@paysy.com',
                                                 customer=buyer,
                                                 pay_gateway=gateway,
                                                 config_name='zona_pagos',
                                                 details='transfer details',
                                                 status='surname',
                                                 value=134.34,
                                                 tax=5.0,
                                                 total=20.5,
                                                 pay_details="payment details",
                                                 )

        return transaction

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@paysy.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = "test@PAYSY.COM"
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test123")

    def test_create_new_super_user(self):
        """Test creating a new super user"""
        user = get_user_model().objects.create_super_user(
            'test@paysy.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_buyer(self):
        """Test creating a new customer"""
        buyer = self.create_customer()
        buyer_db = Customer.objects.get(email='test@paysy.com')

        self.assertEqual(buyer_db, buyer)

    def test_create_pay_gateway(self):
        """Test create a new paymente gateway"""
        user = get_user_model().objects.create_user(
            email="test@paysy.com",
            password="test123"
        )
        gateway = PayGateWay.objects.create(name='testGateway',
                                            prefix='test')
        gateway.site.add(user)
        gateway_db = PayGateWay.objects.get(name='testGateway')

        self.assertEqual(gateway_db, gateway)

    def test_create_transaction(self):
        """Test the creation of a transaction"""
        transaction = self.create_transaction()
        transaction_db = Transaction.objects.get(id_pago='test@paysy.com')

        self.assertEqual(transaction_db, transaction)

    def test_create_zona_pagos_param(self):
        """Test creating zona pagos parameters"""
        param = ZonaPagosParam.objects.create(code=50,
                                              description='Código de '
                                                          'servicio Personal: '
                                                          'Define la '
                                                          'configuración '
                                                          'adicional '
                                                          'que puede tener '
                                                          'el comercio',
                                              payment=False
                                              )
        param_db = ZonaPagosParam.objects.get(code=50)

        self.assertEqual(param, param_db)

    def test_create_zona_pagos_config(self):
        """Test creating zona pagos configuration"""
        config = ZonaPagosConfig.objects.create(int_id_comercio=1234,
                                                id_comercio=1234,
                                                str_usuario="abcd 123",
                                                str_clave="abcd 123",
                                                int_modalidad=123,
                                                payment_url="https://www"
                                                            ".zonapagos.com"
                                                            "/Apis_CicloPago"
                                                            "/api/InicioPago",
                                                consult_url="https://www"
                                                            ".zonapagos.com"
                                                            "/Apis_CicloPago"
                                                            "/api "
                                                            "/VerificacionPago"
                                                )
        config_db = ZonaPagosConfig.objects.get(int_id_comercio=1234)

        self.assertEqual(config, config_db)

    def test_create_zona_pagos(self):
        """Test creating zona pagos"""
        user = get_user_model().objects.create_user(
            email="test@paysy.com",
            password="test123"
        )
        gateway = PayGateWay.objects.create(name='testGateway',
                                            prefix='test')
        gateway.site.add(user)
        config = ZonaPagosConfig.objects.create(int_id_comercio=1234,
                                                id_comercio=1234,
                                                str_usuario="abcd 123",
                                                str_clave="abcd 123",
                                                int_modalidad=123,
                                                payment_url="https://www"
                                                            ".zonapagos.com"
                                                            "/Apis_CicloPago"
                                                            "/api/InicioPago",
                                                consult_url="https://www"
                                                            ".zonapagos.com"
                                                            "/Apis_CicloPago"
                                                            "/api "
                                                            "/VerificacionPago"
                                                )
        param = ZonaPagosParam.objects.create(code=50,
                                              description='Código de '
                                                          'servicio Personal: '
                                                          'Define la '
                                                          'configuración '
                                                          'adicional '
                                                          'que puede tener '
                                                          'el comercio',
                                              payment=False
                                              )
        zona_pagos = ZonaPagos.objects.create(gateway=gateway,
                                              configuration=config,
                                              name='zona_pagos'
                                              )
        ZonaPagosParamVal.objects.create(zona_pagos=zona_pagos,
                                         zona_pagos_param=param,
                                         value="1")
        zona_pagos_db = ZonaPagos.objects.get(gateway=gateway,
                                              configuration=config,
                                              name='zona_pagos'
                                              )
        self.assertEqual(zona_pagos, zona_pagos_db)
