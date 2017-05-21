# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-13 11:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0005_auto_20161111_2311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoiceproduct',
            name='product_id',
        ),
        migrations.AddField(
            model_name='invoiceproduct',
            name='product_serial',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
