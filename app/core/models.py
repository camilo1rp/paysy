from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """Creates and saves a new user"""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that support using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    domain = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'


class PayGateWay(models.Model):
    """Payment gateway model that contains basic information"""
    site = models.ManyToManyField('User', related_name='payways')
    name = models.CharField(max_length=255)
    prefix = models.CharField(max_length=4)
    is_active = models.BooleanField(default=True)


class ZonaPagos(models.Model):
    """Zona Pagos gateway setup"""
    gateway = models.ForeignKey('PayGateWay',
                                on_delete=models.CASCADE,
                                related_name='zona_pagos'
                                )
    configuration = models.ForeignKey('ZonaPagosConfig',
                                      on_delete=models.SET_NULL,
                                      null=True,
                                      related_name='zona_pagos'
                                      )
    parameters = models.ManyToManyField('ZonaPagosParam',
                                        through='ZonaPagosParamVal',
                                        related_name='zona_pagos'
                                        )


class ZonaPagosConfig(models.Model):
    """Zona Pagos gateway config"""
    int_id_comercio = models.PositiveIntegerField()
    str_usuario = models.CharField(max_length=255)
    str_clave = models.CharField(max_length=255)
    int_modalidad = models.SmallIntegerField(default=-1)
    payment_url = models.CharField(max_length=255)
    consult_url = models.CharField(max_length=255)


class ZonaPagosParam(models.Model):
    """Zona Pagos Parameters"""
    code = models.SmallIntegerField()
    description = models.CharField(max_length=511)
    payment = models.BooleanField(help_text="True: payment parameter,"
                                            " False: configuration parameter",
                                  default=False)


class ZonaPagosParamVal(models.Model):
    """Zona Pagos Parameters intermediate table with values"""
    zona_pagos = models.ForeignKey('ZonaPagos',
                                   on_delete=models.CASCADE
                                   )
    zona_pagos_param = models.ForeignKey('ZonaPagosParam',
                                         on_delete=models.CASCADE
                                         )
    value = models.CharField(max_length=255)
