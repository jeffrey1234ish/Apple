# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-18 16:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0037_auto_20170219_0047'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sales',
            old_name='name',
            new_name='sales_name',
        ),
    ]
