from django.contrib import admin

# Register your models here.
from core import models

admin.site.register(models.Customer)
admin.site.register(models.Transaction)
admin.site.register(models.PayGateWay)
admin.site.register(models.ZonaPagos)
admin.site.register(models.ZonaPagosParam)
admin.site.register(models.ZonaPagosConfig)
admin.site.register(models.ZonaPagosParamVal)
