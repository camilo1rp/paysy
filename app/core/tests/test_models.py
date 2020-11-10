from django.test import TestCase
from django.contrib.auth import get_user_model

from core.models import Customer

from core.models import PayGateWay

from core.models import Transaction


class ModelTests(TestCase):

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
        """Test creatin a new customer"""
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
        user = get_user_model().objects.create_user(
            email="test@paysy.com",
            password="test123"
        )
        gateway = PayGateWay.objects.create(name='testGateway',
                                            prefix='test')
        gateway.site.add(user)
        transaction = Transaction.objects.create(id_pago='test@paysy.com',
                                                 customer=buyer,
                                                 paygateway=gateway,
                                                 details='transfer details',
                                                 status='surname',
                                                 value=134.34,
                                                 tex=5.0,
                                                 total=20.5,
                                                 pay_details="payment details",
                                                 )
        transaction_db = Transaction.objects.get(id_pago='test@paysy.com')

        self.assertEqual(transaction_db, transaction)
