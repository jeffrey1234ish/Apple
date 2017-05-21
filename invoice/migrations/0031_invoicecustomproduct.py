# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-05 19:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0030_auto_20161227_2344'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvoiceCustomProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_id', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=50)),
                ('quantity', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
                ('side_note', models.CharField(default=b'', max_length=50)),
                ('color', models.CharField(default=b'', max_length=10)),
            ],
        ),
    ]