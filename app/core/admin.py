from django.contrib import admin


from core import models


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'surname',
                    'document_type', 'document', 'phone')


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id_pago', 'pay_details', 'status',
                    'customer', 'total', 'details', 'create_date')


@admin.register(models.PayGateWay)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('name', 'prefix', 'is_active')


@admin.register(models.ZonaPagos)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('name', 'gateway', 'configuration')


@admin.register(models.ZonaPagosParam)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'payment')


@admin.register(models.TransactionStatus)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'status', 'details', 'created_date')


@admin.register(models.ZonaPagosParamVal)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('zona_pagos', 'zona_pagos_param', 'value')


@admin.register(models.ZonaPagosConfig)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('int_id_comercio', 'id_comercio', 'str_usuario',
                    'str_clave', 'int_modalidad', 'payment_url', 'consult_url')
