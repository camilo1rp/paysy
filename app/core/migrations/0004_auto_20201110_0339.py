# Generated by Django 3.1.3 on 2020-11-10 03:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20201107_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='zonapagosconfig',
            name='id_comercio',
            field=models.PositiveIntegerField(default=2, help_text='Id given by Zona Pagos'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='zonapagosconfig',
            name='int_id_comercio',
            field=models.PositiveIntegerField(help_text='Id given by Zona Virtual'),
        ),
    ]