# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-27 15:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0029_invoice_remaining'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='first_created',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='last_update',
            field=models.DateTimeField(),
        ),
    ]
