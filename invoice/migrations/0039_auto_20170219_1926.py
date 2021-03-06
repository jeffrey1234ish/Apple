# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-19 11:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0038_auto_20170219_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoicecustomproduct',
            name='color',
            field=models.CharField(default=b'', max_length=50),
        ),
        migrations.AlterField(
            model_name='invoicecustomproduct',
            name='invoice_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.Invoice'),
        ),
        migrations.AlterField(
            model_name='invoiceproduct',
            name='invoice_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.Invoice'),
        ),
        migrations.AlterField(
            model_name='invoiceproduct',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.Product'),
        ),
    ]
