from django import forms

from core.models import PayGateWay, ZonaPagosConfig, ZonaPagos

NA = "0"
CC = "1"
CE = "2"
NIT = "3"
NUIP = "4"
TI = "5"
PP = "6"
IDC = "7"
CEL = "8"
RC = "9"
DE = "10"
OT = "11"

DOCUMENT_TYPES = [
    (NA, 'No aplica'),
    (CC, 'Cedula de Ciudadanía'),
    (CE, 'Cedula de Extranjería'),
    (NIT, 'Nit Empresa'),
    (NUIP, 'Número Único de Identificación'),
    (TI, 'Tarjeta de Identidad'),
    (PP, 'Pasaporte'),
    (IDC, 'Identificador Único del Cliente'),
    (CEL, 'Número Celular'),
    (RC, 'Registro Civil de Nacimiento'),
    (DE, 'Documento de Identificación Extranjero'),
    (OT, 'Otro no tipificado'),
]


class PaymentForm(forms.Form):
    """Form for payment test"""

    pay_gateway = forms.ModelChoiceField(queryset=PayGateWay.objects.all(),
                                         label='Pasarela')
    config_name = forms.ModelChoiceField(label='configuración',
        queryset=ZonaPagos.objects.all())
    id_pago = forms.CharField(max_length=63, label="Id de Pago")
    pay_details = forms.CharField()
    document_type = forms.ChoiceField(choices=DOCUMENT_TYPES,
                                      label='Tipo de Documento'
                                      )
    document = forms.CharField(max_length=27, label='Documento')
    email = forms.EmailField()
    name = forms.CharField(max_length=63, label='Nombre')
    surname = forms.CharField(max_length=63, label='Apellido')
    phone = forms.IntegerField(label='Teléfono')
    tax = forms.IntegerField(initial=19, label='IVA')
    total = forms.IntegerField(label='Total')
