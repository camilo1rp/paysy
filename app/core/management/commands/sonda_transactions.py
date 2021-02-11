import datetime
import requests

from django.core.management import BaseCommand
from django.utils import timezone
from rest_framework.renderers import JSONRenderer

from core.models import Transaction, ZonaPagos, TransactionStatus


class Command(BaseCommand):
    help = 'This command checks the status of the transactions on pending ' \
           'and update the state'

    def handle(self, *args, **options):
        transactions = Transaction.objects.filter(status='pending')
        if transactions:
            print("Transactions pending found")
            for trans in transactions:
                zona_pagos = ZonaPagos.objects.get(gateway=trans.pay_gateway,
                                                   name=trans.config_name)
                payload = {
                    "int_id_comercio":
                        zona_pagos.configuration.int_id_comercio,
                    "str_usr_comercio": zona_pagos.configuration.str_usuario,
                    "str_pwd_comercio": zona_pagos.configuration.str_clave,
                    "str_id_pago": trans.id_pago,
                    "int_no_pago": -1
                }
                url = zona_pagos.configuration.consult_url
                headers = {'Content-Type': 'application/json'}
                serialized_json = JSONRenderer().render(payload)
                response = requests.post(url, headers=headers,
                                         data=serialized_json)
                data = response.json()
                status = {'1': 'Finished OK',
                          '2': 'pending',
                          '200': 'started',
                          '777': 'declined',
                          '888': 'pending',
                          '999': 'pending', # banco no ha dado respuesta
                          '4001': 'pending',
                          '4000': 'rejected CR',
                          '4003': 'error CR',
                          '1000': 'rejected',
                          '1001': 'Error between ACH and bank',
                          '1002': 'rejected',
                          }
                pagos_str = data['str_res_pago']
                pagos_split = pagos_str.split(' ; ')[:-1]
                res_status = ""
                pago_finished = ''
                for pago in pagos_split:
                    pago_split = pago.split(' | ')
                    pago_finished = pago_split[3]
                    res_status = pago_split[4]

                status_current = status[res_status]
                if status_current == 'pending':
                    time_compare = trans.create_date + \
                                   datetime.timedelta(seconds=120)
                    if time_compare < timezone.now() and pago_finished == '1':
                        status_current = 'rejected - timeout'

                trans.status = status_current
                trans.details = data['str_detalle']
                trans.save()

                status_trans, _ = TransactionStatus.objects.get_or_create(
                    transaction=trans,
                    status=status_current,
                    details=data['str_detalle']
                )
                status_trans.create_date = datetime.datetime.now()
                status_trans.save()
        print("Transactions updated")
