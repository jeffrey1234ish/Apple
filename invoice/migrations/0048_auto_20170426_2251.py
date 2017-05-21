# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-26 14:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0047_invoice_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('branch_id', models.AutoField(primary_key=True, serialize=False)),
                ('address', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='sales',
            name='branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='invoice.Branch'),
        ),
    ]
