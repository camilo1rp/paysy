from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_super_user(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that support using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    domain = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'


class Customer(models.Model):
    """Custom model that contains the buyer information"""
    email = models.EmailField(max_length=255)
    document_type = models.CharField(max_length=255)
    document = models.CharField(max_length=255)
    name = models.CharField(max_length=127)
    surname = models.CharField(max_length=127)
    phone = models.BigIntegerField()
    extra_field_1 = models.CharField(max_length=127)
    extra_field_2 = models.CharField(max_length=127)
    extra_field_3 = models.CharField(max_length=127)
    extra_field_4 = models.CharField(max_length=127)
    extra_field_5 = models.CharField(max_length=127)

    def __str__(self):
        return f'Customer: {self.name} {self.surname}, {self.email} '


class PayGateWay(models.Model):
    """Payment gateway model that contains basic information"""
    site = models.ManyToManyField('User', related_name='payways')
    name = models.CharField(max_length=255)
    prefix = models.CharField(max_length=4)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Payment Gateways"

    def __str__(self):
        return f'Gateway: {self.name}'


class ZonaPagos(models.Model):
    """Zona Pagos gateway setup"""

    name = models.CharField(max_length=127, unique=True)
    gateway = models.ForeignKey('PayGateWay',
                                on_delete=models.CASCADE,
                                related_name='zona_pagos'
                                )
    configuration = models.ForeignKey('ZonaPagosConfig',
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      related_name='zona_pagos'
                                      )
    parameter = models.ManyToManyField('ZonaPagosParam',
                                       through='ZonaPagosParamVal',
                                       related_name='zona_pagos'
                                       )

    class Meta:
        verbose_name_plural = 'Zona Pagos'

    def __str__(self):
        return f'Zona Pagos: {self.name}'


class ZonaPagosConfig(models.Model):
    """Zona Pagos gateway config"""
    int_id_comercio = models.PositiveIntegerField(
        help_text="Id given by Zona Virtual")
    id_comercio = models.PositiveIntegerField(
        help_text="Id given by Zona Pagos")
    str_usuario = models.CharField(max_length=255)
    str_clave = models.CharField(max_length=255)
    int_modalidad = models.SmallIntegerField(default=-1)
    payment_url = models.CharField(max_length=255)
    consult_url = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Zona Pagos Configurations"

    def __str__(self):
        return f'Zona Pagos Config: {self.int_id_comercio}'


class ZonaPagosParam(models.Model):
    """Zona Pagos Parameters"""
    code = models.SmallIntegerField()
    description = models.CharField(max_length=511)
    payment = models.BooleanField(help_text="True: payment parameter,"
                                            " False: configuration parameter",
                                  default=False)

    class Meta:
        verbose_name_plural = "Zona Pagos parameters"

    def __str__(self):
        return f'Code: {self.code}'


class ZonaPagosParamVal(models.Model):
    """Zona Pagos Parameters intermediate table with values"""
    zona_pagos = models.ForeignKey('ZonaPagos',
                                   on_delete=models.CASCADE
                                   )
    zona_pagos_param = models.ForeignKey('ZonaPagosParam',
                                         on_delete=models.CASCADE,
                                         )
    value = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Zona Pagos parameters values"

    def __str__(self):
        return f'{self.zona_pagos_param}: {self.value}'


class Transaction(models.Model):
    """Transaction model"""
    id_pago = models.CharField(max_length=255, unique=True)
    customer = models.ForeignKey('Customer',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='transactions'
                                 )
    pay_gateway = models.ForeignKey('PayGateWay',
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    related_name='paygateways'
                                    )
    config_name = models.CharField(max_length=127)
    details = models.CharField(max_length=511, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    value = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    tax = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    pay_details = models.CharField(max_length=511)
    create_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Transaction: {self.id_pago}'


class TransactionStatus(models.Model):
    """Transaction status"""
    transaction = models.ForeignKey('Transaction',
                                    on_delete=models.CASCADE,
                                    related_name='statustrans'
                                    )
    status = models.CharField(max_length=63)
    details = models.CharField(max_length=511)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Transaction Status"

    def __str__(self):
        return f'{self.transaction}: {self.status}'
