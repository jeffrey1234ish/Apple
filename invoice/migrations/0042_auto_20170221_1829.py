# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-21 10:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0041_auto_20170219_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Oak',
            field=models.BooleanField(default=False),
        ),
    ]
