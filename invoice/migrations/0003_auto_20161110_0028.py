# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-09 16:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0002_auto_20161109_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='additional_note',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='discount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='invoice_id',
            field=models.AutoField(default=60000, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_amount',
            field=models.IntegerField(default=0),
        ),
    ]
