# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-18 16:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0036_auto_20170123_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('name', models.CharField(max_length=30)),
                ('sales_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.AddField(
            model_name='invoice',
            name='payment_type',
            field=models.CharField(choices=[(b'V', b'Visa'), (b'E', b'EPS'), (b'C', b'Cash')], default=b'C', max_length=1),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='sales',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.Sales'),
        ),
    ]
