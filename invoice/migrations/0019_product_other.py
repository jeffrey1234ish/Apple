# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 14:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0018_auto_20161129_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Other',
            field=models.BooleanField(default=False),
        ),
    ]
