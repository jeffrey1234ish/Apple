# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-25 10:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0009_invoice_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='price',
            new_name='raw_price',
        ),
    ]
